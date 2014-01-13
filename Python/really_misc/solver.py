"""
This class is intended to act as a framework for setting up workforce placement
models run on a SQL type database backend
"""
import sys
import os
import re
import itertools
import web_deploy
import datetime
import pickle

import numpy as np
import pandas as pa
import numpy.random as rand

#This is just until this is an installed application
sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "web_deploy.web_deploy.settings")

from pandas.io import sql
from pandas.tools.pivot import pivot_table

import ipdb

##useful functions
def get_model_fields(model):
    """
    Gets fields of model object

    Parameters
    ----------
    model : Django model object

    Returns
    -------
    list
    """
    fields = [full_field.name for full_field in model._meta.fields
                  if full_field.name != 'id']
    return fields

def update_db(dframe, model, fields):
    """
    Updates db with fields from dframe

    Parameters
    ----------
    dframe : pandas DataFrame
        Source DataFrame with data
    model : Django model object
        Model to update from DataFrame
    fields : list
        Fields to update
    """
    elements = [dframe[field] for field in fields]
    row = model.create(*elements)
    row.save()

def transform(field):
    """
    Transforms field into proper value for SQL
    """
    if type(field) == str:
        return "'" + str(field) + "'"
    else:
        return str(field)

def to_list(value):
    """
    Transform to list if not already list
    """
    if type(value) != list:
        return [value]
    else:
        return value

def match_fields_gen(rules):
    """
    Generate list of unique fields from rules given
    """
    match_fields = []
    for rule in rules:
        if rule['OF'] not in match_fields:
            match_fields.append(rule['OF'])
        if rule['NF'] not in match_fields:
            match_fields.append(rule['NF'])
    return match_fields

class TableDoesNotExist(Exception):
    """
    Error class to return when table does not exist
    """
    def __init__(self, table):
        self.table = table
    def __str__(self):
        return repr("Table '" + self.table + "' does not exist in database!")

class PlacModel(object):
    """
    This class initiates an object
    """
    #!!!! Should change table names to dictionary so function arguments
    #aren't too many. This also makes sense for making certain table
    #inputs optional.
    def __init__(self, cnxn, rules, empl_table="Employees", pos_table="Positions",
                 distance_table="Distances", attrit_table="Attrition",
                 closings_table="Closings", locations_table="Locations",
                 pothires_table="PotentialHires", excess_code=-999999,
                 in_mem=True, sql_type='ODBC'): 
        """
        This function initiates the PlacModel object and loads all of
        the key connections

        Parameters
        ----------
        cnxn : SQL connection object
            For testing, ODBC connection object was used

        rules: list of dicts
            Lists rules defined using rule mappings rule attributes:
                OF -> original field (from vacancies)
                NF -> new field (from available positions)
                operator -> operator (see below)
                OV -> old value(s) (values from vacancies for manual
                      mappings)
                NV -> new value(s) (values from available positions for
                      manual mappings)

            operator in ('=', '>', '>=', '<', '<=', 'in')
                '=' -> equals
                '>' -> greater than
                '>=' -> greater than or equal to 
                '<' -> less than
                '<=' -> less than or eqaul to
                'in' -> within range

            If both OV and NV are included, manual matches are
            performed.
            If only OV is included, then the operation is only performed
            on this subset of old values.
            If only NV is included, then the operation is only performed
            on this subset of new values.

            These rules replace intra_field_map and match_field from
            v0.1.

        empl_table: string, default "Employees"
            Name of Employment table in source database, containing all
            employees

            Should have at least the following fields:
                employee: int
                position: int
                location: int
                *match_fields

        pos_table: string, default "Positions"
            Name of Positions table in source database, containing all
            available positions

            Should have at least the following three fields:
                position: int
                location: int
                *match_fields

        distance_table: string, default "Distances"
            Name of Distances table in source database, containing
            distances between any two centers

            Should have at least the following three fields:
                location: int
                destination: int
                distance: float

        attrit_table: string, default "Attrition"
            Name of Attrition table in source database, containing
            attrition rates for each match_field group in each period

            Should have at least the following three fields:
                period: int
                rate: float
                *match_fields

        closings_table: string, default "Closings"
            Name of Closings table in source database, containing
            closing
            locations by period
                location: int
                period: int

        locations_table: string, default "Locations"
            Name of Locations table, maps locations to other geographies
                location: int

        pothires_table: string, default "PotentialHires"
            Name of Potential Hires table, has hires available on the
            market
                hireid: int (key)
                location: int
                *match_fields

        excess_code: int, default -999999
            code signifying employee is unemployed

        in_mem: boolean
            Whether processing should be performed in memory using
            pandas or in server-side SQL
            In-memory processing is more efficient but can fail if the
            source data is too big.

        """
        self.cnxn = cnxn
        self.excess_code = excess_code
        self.sql_type = sql_type
        self.in_mem = in_mem
        self.pos_table = pos_table
        self.empl_table = empl_table
        self.distance_table = distance_table
        self.attrit_table = attrit_table
        self.closings_table = closings_table
        self.locations_table = locations_table
        self.pothires_table = pothires_table
        
        self.rules = rules
        self.match_fields = match_fields = match_fields_gen(rules)

        self.sql_dir = os.path.join(os.path.split(web_deploy.__file__)[0],
                                    "..",
                                    "model_frame",
                                    "native_sql")

        key_tables = [empl_table, pos_table, distance_table, closings_table,
                      attrit_table]

        #Check if all tables exist in database
        cursor = cnxn.cursor()
        self._check_tables(cursor, key_tables)

        if in_mem:
            #Read all table into pandas dataframes
            self.empl_df = self._read_from(empl_table, cnxn)
            self.empl_df = self.empl_df[['employee', 'position',
                                         'location'] + match_fields]
            self.empl_df.set_index('employee', inplace=True,
                                   verify_integrity=True)
            self.empl_ix = self.empl_df.reset_index()['employee'].max()

            self.pos_df = self._read_from(pos_table, cnxn)
            self.pos_df = self.pos_df[['position', 'location'] + match_fields]
            self.pos_df.set_index('position', inplace=True,
                                  verify_integrity=True)
            self.pos_ix = self.pos_df.reset_index()['position'].max()

            self.pothires_df = self._read_from(pothires_table, cnxn)
            self.pothires_df = self.pothires_df[['hireid', 'location'] +
                                                match_fields]
            self.pothires_df.set_index('hireid', inplace=True,
                                       verify_integrity=True)

            distance_df = self._read_from(distance_table, cnxn)
            self.distance_df = distance_df[distance_df['distance'] > 0]
            self.attrit_df = self._read_from(attrit_table, cnxn)
            self.closings_df = self._read_from(closings_table, cnxn)
            self.locations_df = self._read_from(locations_table, cnxn)
            self.locations_df.set_index('location', inplace=True,
                                        verify_integrity=True)
            #prepare summary table
            self.summary_df = pa.DataFrame(
                                  columns=['period', 'location'] +
                                          match_fields +
                                          ['total', 'excess', 'vacancies']
                                      ).set_index(
                                          ['period', 'location'] +
                                          match_fields)
            cursor.close()
        else:
            self._refresh_sql()
        #maybe disconnect from database here
        print "Model intialization success"

    def run_model(self, periods=1, dist_rest=None, rules=[],
                  summ_group="district"):
        """
        !!!!This needs to be updated. Not even sure if this applicable
        anymore

        This function runs the model given the parameters specified in
        the initialization of the PlacModel object and using the default
        run order for the different tasks specified in other functions

        periods: int, default 1
            Number of periods to run the model

        dist_rest: float, default None
            Distance restriction on moving

        rules

        summ_group: string or list of strings, default []
            Groups to summarize by in summary table repopulated in
            source database
        """
        raise NotImplementedError('This method should be customized')

    def validate_data(self):
        """
        !!!! This should be implemented
        Validates the data
        """
        raise NotImplementedError('Data validation not yet available')

    def attrit(self, period):
        """
        Removes those employees that retire and opens up their positions

        Parameters
        ----------

        periods: int
            Period to run the model in
        """
        if self.in_mem:
            empl_cols = self.empl_df.columns
            pos_cols = self.pos_df.columns
            match_fields = self.match_fields

            #generate random number 0-1
            self.empl_df["ret_act"] = rand.random(len(self.empl_df))
            #subset attrition to period
            attrit_per = self.attrit_df[self.attrit_df['period'] == period]
            #merge with employees file
            attrit_emp_join = self.empl_df.reset_index().merge(
                                  attrit_per,
                                  on=match_fields).set_index('employee')
            #get retiring people for this period
            retiring_df = attrit_emp_join[
                attrit_emp_join['ret_act'] <= attrit_emp_join['rate']
                ]

            #remove them from list of employees
            self.empl_df = attrit_emp_join[
                attrit_emp_join['ret_act'] > attrit_emp_join['rate']
                ][empl_cols]

            self.pos_df = pa.concat([
                self.pos_df,
                retiring_df.reset_index().set_index('position')])[pos_cols]

        else:
            self._attrit_sql(period)

    def close_facs(self, period):
        """
        Set employees to unemployed where faciilites close and remove
        available positions from those closing faciilites

        Parameters
        ----------

        periods : int
            What period to grab closing locations from
        """
        if self.in_mem:
            empl_cols = self.empl_df.columns
            pos_cols = self.pos_df.columns
            excess_code = self.excess_code

            #grab closing locations this period
            close_locs = self.closings_df[
                            self.closings_df['period'] == period
                            ][['location']]
            if len(close_locs):
                #set their position to excess_code
                close_locs['position'] = excess_code

                #set closing location employees to unemployed
                self.empl_df = self.empl_df.reset_index().merge(
                                   close_locs,
                                   on=['location'],
                                   how='left',
                                   suffixes=('_orig',
                                             '_closed')
                                   ).set_index('employee')
                code_pos = lambda df: df['position_orig'] \
                            if (np.isnan(df['position_closed'])) \
                                else df['position_closed']
                self.empl_df['position'] = self.empl_df.apply(
                                              code_pos,
                                              axis=1)
                self.empl_df = self.empl_df[empl_cols]

                #remove open positions from these closing locations
                close_locs = close_locs.rename(
                                 columns={'position':'position_empty'}
                              )
                self.pos_df = self.pos_df.reset_index().merge(close_locs,
                                                              on=['location'],
                                                              how='left'
                                                             )
                self.pos_df = self.pos_df[np.isnan(
                    self.pos_df['position_empty'])]
                self.pos_df = self.pos_df.set_index('position')
                self.pos_df = self.pos_df[pos_cols]

        else:
            self._close_facs_sql(period)

    def move_people(self, rule_en, hire=False, dist_rest=None):
        """
        Move available employees or hires to open positions

        Parameters
        ----------
        rule_en: list
            Lists the rule number to implement. Each is implemented
            completely each time this is called.

        hire: boolean
            Internal employee movement or external hiring

        dist_rest : float, default None
            Maximum moving distance for employee from previous place of
            employment

        inter_field : boolean, default False
            Attempt matching simulataneously across multiple fields
        """
        if self.in_mem:

            #set distance restriction
            if dist_rest:
                viabdistance_df = self.distance_df[
                                      self.distance_df['distance'] < 
                                          dist_rest]

            empl_cols = self.empl_df.columns
            pos_cols = self.pos_df.columns

            #change to 0 indexing
            rule_indexes = [el - 1 for el in rule_en]
            step_rules = [self.rules[ix] for ix in rule_indexes]

            people, key, assign_func = self._gen_people(hire, step_rules)

            if len(people):
                #grab all locations for these unemployed people within 50 miles
                #of their original location
                people_wdest = people.reset_index().merge(viabdistance_df,
                                                             on=['location'])

                #only need to try and match people if there are potential move
                #locations for these people
                if len(people_wdest):

                    #create destination column
                    poses = self._gen_positions(step_rules)

                    all_matches = people_wdest.merge(
                                      poses.reset_index(),
                                      on=['destination'],
                                      suffixes=('_from_peop',
                                                '_from_pos'))

                    for rule in step_rules:
                        all_matches = self._apply_rule(all_matches, rule)

                    #sort to get top position first
                    #evenutually make this subject to user input
                    all_matches.sort(columns=['distance'], inplace=True)

                    #if there is a position availablle
                    while len(all_matches):

                        #assign available position
                        all_matches = assign_func(all_matches)

                        #only keep necessary columns in pos_df and empl_df
                        #!!!! might be able to drop these two lines
                        self.pos_df = self.pos_df[pos_cols]
                        self.empl_df = self.empl_df[empl_cols]

        else:
            self._move_people_sql(hire, dist_rest, intra_field_map,
                                  inter_field)

    def update_summary(self, period):
        """
        Updates summary dataframe with summary information for this
        group

        Parameters
        ----------
        period : int
            Period to add information for into Summary table
        gropup : string or list of strings
            Indicates fields to groupby in Summary table
            These group fields must be kept in locations_table
        """
        if self.in_mem:
            excess_code = self.excess_code
            match_fields = self.match_fields
            groups = ['location'] + match_fields

            #Total employees
            loc_tot = pa.DataFrame(self.empl_df.groupby(groups).size()
                                        ).rename(columns={0: 'total'})

            #count excess
            excess_empl = self.empl_df[self.empl_df['position'] == excess_code]
            if len(excess_empl):
                loc_exc = pa.DataFrame(excess_empl.groupby(groups).size()
                                        ).rename(columns={0: 'excess'})

            else:
                loc_exc = pa.DataFrame(index=self.locations_df.index)
                loc_exc['excess'] = 0

            #count vacancies
            if len(self.pos_df):
                loc_vac = pa.DataFrame(self.pos_df.groupby(groups).size()
                                          ).rename(columns={0: 'vacancies'})
            else:
                loc_vac = pa.DataFrame(index=self.locations_df.index)
                loc_vac['vacancies'] = 0

            #join into single DF
            loc_summ = loc_tot.join(loc_vac, how='outer').join(
                           loc_exc).reset_index().fillna(0)
            loc_summ['period'] = period
            self.summary_df = pa.concat([self.summary_df, 
                                  loc_summ.set_index(
                                      ['period', 'location'] + match_fields)])
        else:
            self._update_summary_sql(period)

    def save_run(self, run_numb, save_dir='C:/Users/babaker/Plac_Runs',
                     user='anonymous'):
        """
        Function that saves pickled run in directory
        This function removes the connection object

        !!!!For now, remove all tables except summary_df
        """
        if self.in_mem:
            #determine path of variable
            dir_path = os.path.join(save_dir, user, "temp/")
            #create path if it doesn't exist
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            current_time = datetime.datetime.now()
            file_name = re.sub("[:|\/]", ".",
                    current_time.strftime("date_%x_time_%X_run_{numb}.pmr").format(
                        numb=str(run_numb)))
            full_path = os.path.join(dir_path, file_name)

            #Remove connection and excess df objects
            #!!!! This should eventually depend on the optional tables provided
            del self.cnxn
            del self.empl_df
            del self.pos_df
            del self.pothires_df
            del self.distance_df
            del self.locations_df

            #pickle to path
            pickle.dump(self, open(full_path, 'wb'))

            return full_path

        else:
            return NotImplementedError("Need to implement saving SQL runs")


    def _assign_is(self, avail_pos):
        """
        Assign available position to current employee
        """
        empl_cols = self.empl_df.columns

        #grab the closest matching position
        pos = avail_pos[:1]

        #reset position and location
        for field in empl_cols:
            pos[field] = pos[field + '_from_pos']

        position, employee = pos[['position', 'employee']].values[0].tolist()

        #remove position from positions DF
        self.pos_df = self.pos_df.drop([position])

        ##change status of that employee to employed
        empl_update = pos[['employee'] + empl_cols.tolist()].set_index(
                                                             'employee')
        self.empl_df.update(empl_update, join='left',
                            overwrite=True)

        #remove dropped rows from avail_pos
        avail_pos = avail_pos.loc[
                        (avail_pos['position_from_pos'] != position) &
                        (avail_pos['employee'] != employee)]

        return avail_pos

    def _assign_es(self, avail_pos):
        """
        Assign available position to new hire
        """
        empl_cols = self.empl_df.columns
        match_fields = self.match_fields

        #grab the closest matching position
        pos = avail_pos[:1]

        ##reset position and location
        #assigning position to employee
        pos['location'] = pos['location_from_pos']
        position, hireid = pos[['position', 'hireid']].values[0].tolist()

        #remove position from positions DF
        self.pos_df = self.pos_df.drop([position])

        #remove hiree from potential hires table
        self.pothires_df = self.pothires_df.drop([hireid])

        #add this hire to employed
        both_fields = match_fields + ['location']
        empl_update = pos[[el +'_from_pos' for el in both_fields] +
                          ['position']]
        for field in both_fields:
            empl_update[field] = empl_update[field + '_from_pos']
        self.empl_ix += 1
        empl_update['employee'] = self.empl_ix
        empl_update.set_index('employee', inplace=True)
        empl_update = empl_update[empl_cols]

        #!!!! this isn't great for performance, come back to this
        self.empl_df = pa.concat([self.empl_df, empl_update],
                                  verify_integrity=True)

        #remove dropped rows from avail_pos
        avail_pos = avail_pos.loc[(avail_pos['position'] != position) &
                                  (avail_pos['hireid'] != hireid)]

        return avail_pos

    def _check_tables(self, cursor, tables):
        """
        Checks if tables exist in database
        """
        sql_type = self.sql_type

        search_table = []

        if sql_type == "ODBC":
            for table in cursor.tables():
                search_table.append(table.table_name)
            for ktable in tables:
                if ktable not in search_table:
                    raise TableDoesNotExist(ktable)

        elif sql_type == "PG":
            cursor.execute("SELECT table_name " +
                            "FROM information_schema.tables " +
                            "WHERE table_schema = 'public'")

            table_check = cursor.fetchall()
            for table in table_check:
                search_table.append(table[0])
            for ktable in tables:
                if ktable not in search_table:
                    raise TableDoesNotExist(ktable)

    def _read_from(self, table, conn):
        """
        Read from table
        """
        get_all = "SELECT * FROM "

        sql_type = self.sql_type

        if sql_type == "PG":
            dframe = sql.read_frame(get_all + '"' + table + '"', conn)

        else:
            dframe = sql.read_frame(get_all + '"' + table + '"', conn)

        return dframe

    def _gen_people(self, hire, step_rules):
        """
        Generate people to potentially move/hire
        """
        match_fields = self.match_fields
        excess_code = self.excess_code

        #hiring, just use current list of potential hires
        if hire:
            people = self.pothires_df
            key = 'hireid'
            assign_func = self._assign_es

        #else grab list of people without jobs
        else:
            #grab unemployed into single DF
            people = self.empl_df[self.empl_df['position'] == excess_code]
            key = 'employee'
            assign_func = self._assign_is

        #grab cross field value mappings
        for rule in step_rules:
            if 'OV' in rule:
                people = people[people[rule['OF']].isin(to_list(rule['OV']))]

        return people, key, assign_func

    def _gen_positions(self, step_rules):
        """
        Generate positions to potentially move/hire for
        """
        poses = self.pos_df
        poses['destination'] = poses['location']

        #grab cross field value mappings
        for rule in step_rules:
            if 'NV' in rule:
                poses = poses[poses[rule['NF']].isin(to_list(rule['NV']))]

        return poses

    def _apply_rule(self, mat, rule):
        """
        Applies rule and limits results of dataset
        """
        orig_field = rule['OF'] + '_from_peop'
        new_field = rule['NF'] + '_from_pos'
        operator = rule['operator']

        # set adjust_pos and adjust_neg to zero if not in rule
        if 'adjust_pos' not in rule:
            rule['adjust_pos'] = 0

        if 'adjust_neg' not in rule:
            rule['adjust_neg'] = 0

        # combine adjust_pos and neg for use with non-in operators
	adjust_tot = rule['adjust_pos'] - rule['adjust_neg']
	
	#!!!! implement adjustments for other operators
		
        #Apply rules
        if ('OV' in rule) and ('NV' in rule):
            orig_value = to_list(rule['OV'])
            new_value = to_list(rule['NV'])
            mat = mat[(mat[orig_field].isin(orig_value)) &\
                      (mat[new_field].isin(new_value))]
        elif operator == '=':
            mat = mat[mat[orig_field] == mat[new_field] - adjust_tot]
        elif operator == '>':
            mat = mat[mat[orig_field] > mat[new_field] - adjust_tot]
        elif operator == '>=':
            mat = mat[mat[orig_field] >= mat[new_field] - adjust_tot]
        elif operator == '<':
            mat = mat[mat[orig_field] < mat[new_field] - adjust_tot]
        elif operator == '<=':
            mat = mat[mat[orig_field] <= mat[new_field] - adjust_tot]
        elif operator == 'in':
            mat = mat[(mat[orig_field] <= (mat[new_field] - \
                      rule['adjust_pos'])) & (mat[orig_field] >= \
                      (mat[new_field] + rule['adjust_neg']))]

        return mat

    def _attrit_sql(self, period):
        """
        Run sql version of attrition code
        """
        cnxn = self.cnxn
        match_fields = self.match_fields

        #create formatted fields
        te_match_fields = ",".join(["TE." + el for el in match_fields])
        att_match_fields = ",".join(["ATT." + el for el in match_fields])
        join_match_fields = " AND ".join(['EMP.' + el + ' = ' + 'ATT.' + el
                                            for el in match_fields])
        matchfields = ",".join(match_fields)

        attrit_string = open(os.path.join(self.sql_dir, 'attrit.sql')).read()
        cursor = cnxn.cursor()
        #create/update SP
        cursor.execute(attrit_string.format(
            te_match_fields=te_match_fields,
            att_match_fields=att_match_fields,
            join_match_fields=join_match_fields,
            matchfields=matchfields))
        cnxn.commit()
        #execute SP
        cursor.execute("{call attrit(" + str(period) + ")}")
        cnxn.commit()

    def _refresh_sql(self):
        """
        Run sql version of attrition code
        """
        cnxn = self.cnxn
        match_fields = self.match_fields

        #create formatted fields
        pos_source = self.pos_table
        emp_source = self.empl_table
        pothire_source = self.pothires_table

        refresh_string = open(os.path.join(self.sql_dir, 'refresh.sql')).read()
        cursor = cnxn.cursor()
        #create/update SP

        matchfields = ",".join(match_fields)
        cursor.execute(refresh_string.format(pos_source=pos_source,
                                             emp_source=emp_source,
                                             pothire_source=pothire_source,
                                             matchfields=matchfields))
        cnxn.commit()
        #execute SP
        cursor.execute("{call RefreshTemps}")
        cnxn.commit()

    def _close_facs_sql(self, period):
        """
        Run sql version of closing facs code
        """
        cnxn = self.cnxn
        excess_code = self.excess_code
        cursor = cnxn.cursor()

        cf_string = open(os.path.join(self.sql_dir, 'Close_Facs.sql')).read()
        cursor.execute(cf_string)
        cnxn.commit()
        #execute SP
        cursor.execute("{call close_facs(" + str(period) + "," +
                       str(excess_code) + ")}")
        cnxn.commit()

    def _move_people_sql(self, hire, dist_rest, intra_field_map, inter_field):
        """
        Run sql version of move people code
        """
        cnxn = self.cnxn
        match_fields = self.match_fields
        excess_code = self.excess_code

        #need to perform specific SQL code building procedures when performing
        #movements
        if intra_field_map:
            if hire:
                select_chunk = open(os.path.join(self.sql_dir,
                                'hire_people_sel.sql')).read()
                sql_file = "Hire_People_Cross"
                tbname = "HireLocations"
                matchfields = ",".join(match_fields)

            else:
                select_chunk = open(os.path.join(self.sql_dir,
                                'move_people_sel.sql')).read()
                sql_file = "Move_People_Cross"
                tbname = "Relocations"
                matchfields = ",".join([field + " = (select top 1 " + field +
                            " from #Openings)" for field in match_fields])

            #SQL chunk will be all combinations of different field mappings if
            #inter_field is True
            if inter_field:
                chunked = self._sql_chunk_inter(sql_file,
                                                tbname,
                                                intra_field_map,
                                                select_chunk)
            else:
                chunked = self._sql_chunk_intra(sql_file,
                                                tbname,
                                                intra_field_map,
                                                select_chunk)


        #Simpler when just performing standard within field/value matching
        else:
            if hire:
                sql_file = "Hire_People"
                tbname = "HireLocations"
                
            else:
                sql_file = "Move_People"
                tbname = "Relocations"

            matchfields = ",".join(match_fields)

            chunked = ' '

        tbmatchfields = ",".join([tbname + "." + el for el in match_fields])
        tbmatchequals = " AND ".join([tbname + "." + el + " = TP." + el 
                                        for el in match_fields])

        sql_text = open(os.path.join(self.sql_dir, sql_file + '.sql')).read()
        cursor = cnxn.cursor()

        cursor.execute(sql_text.format(select_pool=chunked,
                                       matchfields=matchfields,
                                       tbmatchfields=tbmatchfields,
                                       tbmatchequals=tbmatchequals))

        cnxn.commit()
        #execute SP
        if hire:
            cursor.execute("{call " + sql_file + "(" + str(dist_rest) + ")}")
        else:
            cursor.execute("{call " + sql_file + "(" + str(dist_rest) + "," +
                           str(excess_code) + ")}")

        cnxn.commit()

    def _sql_chunk_intra(self, sql_file, tbname, intra_field_map,
                         select_chunk):
        """
        Create chunk of SQL for top of movement within field groups
        """
        match_fields = self.match_fields
        matchfields = ",".join(match_fields)
        tbmatchfields = ",".join([tbname + "." + el for el in match_fields])
        unions = 0

        for field in intra_field_map.iterkeys():
            for orig_value in intra_field_map[field]:
                match_orig = field + " = " + transform(orig_value)

                match_new = "TP." + field + " in " + "(" + \
                            ",".join([transform(value) for value in
                                    intra_field_map[field][orig_value]]) + \
                            ")"
                add_chunk = select_chunk.format(
                                tbmatchfields=tbmatchfields,
                                matchfields=matchfields,
                                match_group_orig=match_orig,
                                match_group_new=match_new)

                if unions:
                    chunked = " UNION \n".join([chunked, add_chunk])
                else:
                    chunked = add_chunk

                unions += 1

        return chunked

    def _sql_chunk_inter(self, sql_file, tbname, intra_field_map,
                         select_chunk):
        """
        Create chucnk of SQL for top of movement across multiple field groups
        """
        match_fields = self.match_fields
        matchfields = ",".join(match_fields)
        tbmatchfields = ",".join([tbname + "." + el for el in match_fields])

        #create interfield object
        inter_field_map = []
        for field in intra_field_map:
            field_map = []
            for maps in intra_field_map[field].iteritems():
                field_map.append((field,) + maps)
            inter_field_map.append(field_map)

        #This creates a list of combinations for the current fields
        #to create SQL chunks for
        inter_field_list = []
        for perm in itertools.product(*inter_field_map):
            inter_field_list.append(perm)

        unions = 0

        for inter_field in inter_field_list:
            match_orig = " AND ".join(
                [field_group[0] + " = " + transform(field_group[1])
                    for field_group in inter_field])

            match_new = " AND ".join(
                ["TP." + field_group[0] + " in " + "(" +
                    ",".join([transform(value)
                        for value in field_group[2]]) + ")"
                            for field_group in inter_field])

            add_chunk = select_chunk.format(
                                tbmatchfields=tbmatchfields,
                                matchfields=matchfields,
                                match_group_orig=match_orig,
                                match_group_new=match_new)

            if unions:
                chunked = " UNION \n".join([chunked, add_chunk])
            else:
                chunked = add_chunk

            unions += 1

        return chunked

    def _update_summary_sql(self, period):
        """
        Submit summary information for this period
        """
        cnxn = self.cnxn
        cursor = cnxn.cursor()
        excess_code = self.excess_code
        match_fields = self.match_fields
        empl_table = self.empl_table
        pos_table = self.pos_table

        us_string = open(os.path.join(self.sql_dir,
                                       'SummaryReport.sql')).read()
        matchfields = ",".join(match_fields)
        elmatchfields = ",".join(["EL." + field for field in match_fields])
        eltpmatchfields = " AND ".join(["EL." + field + " = TP." + field 
                                        for field in match_fields])
        #prepare SP
        cursor.execute(us_string.format(matchfields=matchfields,
                                        elmatchfields=elmatchfields,
                                        eltpmatchfields=eltpmatchfields))
        cnxn.commit()

        #Execute SP
        cursor.execute("{call SummaryReport(" + str(period) + "," +
                      str(excess_code) + ")}")
        cursor.commit()
