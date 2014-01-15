import pyodbc
import sys
import os
import operator

import pandas as pa
import numpy.random as ra

import ipdb

from pandas.io import sql
#this path.append is temporary until becomes fully installed package
sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 
                      "web_deploy.web_deploy.settings")
from web_deploy import modeler
import web_deploy

from model_frame.solver import PlacModel
from model_frame.solver import match_fields_gen
from django.utils.datastructures import SortedDict
# test insert in vim
#for testing
def count_missing(frame):
    count_nas = (frame.shape[0] * frame.shape[1]) - frame.count().sum()
    if count_nas != 0:
        raise Exception("Some NA's here")

#connect to SQL Server database
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.118.4.151;' +
                      'DATABASE=Demos_G500;UID=vaadmin;PWD=va@dmin')

in_mem = True
periods = 8
#cross craft possible 10 to 40 and 40 to 10
dist_rest = 50
rules = []

#seed random number generator for reproducibility
ra.seed(103)

# create columns to sort on for movement between competitive areas
# each column is a key in the dictionary where the value is a tuple
# index 0 of the tuple indicates 'num' for numeric or 'txt' for text
# index 1 is either 1 for asc sort or 0 for desc 

from collections import OrderedDict

sort_col = OrderedDict({'Tenure': ('txt', 1),
            'VetPref': ('txt', 0),
            'AvgRating': ('num', 0),
            'CreditableService': ('num', 0)})

# Create dictionary for determining what supply is impacted

impact_col = {'Mission': 'B'}

# inherit from PlacModel class and modify for gs500

class gs500(PlacModel):
    def __init__(self, cnxn, isupply_table, sort_col, impact_col, rules,
                 id_map={'id_col' : 'EmpID', 'pos_col' : 'PositionNumber',
                         'loc_col' : 'Location', 'time_col' : 'Period'},
                 in_mem = True, sql_type = 'ODBC'):
        self.cnxn = cnxn
        self.isupply_table = isupply_table
        self.sort_col = sort_col
        self.impact_col = impact_col
        self.rules = rules
        self.sql_type = sql_type
        self.in_mem = in_mem
        self.match_fields = match_fields = match_fields_gen(rules)
        
        self._map_key_columns(id_map)
        id_col = self.id_col
        pos_col = self.pos_col
        loc_col = self.loc_col
        time_col = self.time_col

        #!!!! this will need to be conditional on SQL type, i.e. MySQL, PG
        self.sql_dir = os.path.join(os.path.split(web_deploy.__file__)[0],
                                    "..",
                                    "model_frame",
                                    "native_sql")

        #Check if all tables exist in database
        cursor = cnxn.cursor()
        self._check_tables(cursor, [isupply_table])

        if in_mem:
            #Read all table into pandas dataframes
            self.isupply_df = self._read_from(isupply_table, cnxn)
            self.isupply_df.set_index(id_col, inplace=True,
                                   verify_integrity=True)
            self.isupply_ix = self.isupply_df.reset_index()[id_col].max()

            # created impacted_df and update isupply_df
            # drop out Vacant Employees from impacted
            
            self.impacted_df = self.isupply_df[\
            (self.isupply_df['Mission'] == impact_col['Mission']) \
                        & (self.isupply_df['EmployeeName'] <> 'Vacant')]

            self.isupply_df = self.isupply_df[\
                self.isupply_df['Mission'] <> impact_col['Mission']]

            self.no_match_df = self.impacted_df[\
                self.impacted_df['Tenure'] == 'III']

            self.impacted_df = self.impacted_df[\
                self.impacted_df['Tenure'] <> 'III']

            self.transactions_df = pa.DataFrame(\
                columns = ['From_Table', 'To_Table', 'EmployeeID'])
            # Remove step field from other methods
            
            cursor.close()
        else:
            self._refresh_sql()
        #maybe disconnect from database here
        print "Model intialization success"

    def _compare(self, val_1, val_2):
        col_list = list(self.isupply_df.columns)

        for key in self.sort_col.keys():
            key_ind = col_list.index(key)
            if self.sort_col[key][1] == 1:
                op = operator.lt
            else:
                op = operator.gt

            if op(val_1[key_ind], val_2[key_ind]):
                return 1
            elif val_1[key_ind] <> val_2[key_ind]: # if equal continue loop
                return 0

        if val_1[1] > val_2[1]:
            return 1
        else:
            return 0

    def _update_trans(self, person, from_table, to_table):
        """
        Update transaction df

        Parameters
        ----------
        person: list
            list of values from row of data frame that were transferred.

        from_table: data frame
            Name of Data frame initially containing person

        to_table: data frame
            Name of Data frame person moved to.
        """
        row_dict = dict(zip(self.transactions_df.columns, \
                            [person[1], from_table, to_table]))
        self.transactions_df = self.transactions_df.append(\
            row_dict, ignore_index = True)

    def move_people(self):
        """
        Move available employees or hires to open positions

        Parameters
        ----------
        rule_en: list
            Lists the rule number to implement. Each is implemented
            completely each time this is called.

        hire: boolean
            Internal employee movement or external hiring

        inter_field : boolean, default False
            Attempt matching simulataneously across multiple fields
        """
        if self.in_mem:
            sort_keys = sort_col.keys()
            sort_asc = [sort[1] for sort in sort_col.values()]

            self.isupply_df.sort(sort_keys, ascending = sort_asc)

            while len(self.impacted_df):
                self.impacted_df.sort(sort_keys, ascending = sort_asc)
                imp_val = self.impacted_df.irow(0).values
                moved_to_supp = 0
                temp_supp = self.isupply_df[self.isupply_df['OccSeries'] \
                                            == imp_val[6]]
                
                for supp_val in temp_supp.values:
                    if self._compare(imp_val, supp_val): 
                        self.isupply_df[self.isupply_df['EmployeeName'] \
                                        == supp_val[1]] = imp_val
                        supp_val_dict = dict(zip(self.isupply_df.columns, \
                                                 supp_val))
                        self.isupply_df = self.isupply_df[\
                            self.isupply_df['EmployeeName'] <> supp_val[1]]

                        self.impacted_df = self.impacted_df[\
                            self.impacted_df['EmployeeName'] \
                            <> imp_val[1]].append(\
                                supp_val_dict, ignore_index = True)
                                            
                        moved_to_supp = 1
                        self._update_trans(supp_val, 'i_supply', 'impacted')
                        self._update_trans(imp_val, 'impacted', 'i_supply')
                        
                        break # only replace highest instance

                if not moved_to_supp:
                    imp_val_dict = dict(zip(self.impacted_df.columns, imp_val))
        
                    self.impacted_df = self.impacted_df[\
                        self.impacted_df['EmployeeName'] <> imp_val[1]]
                    
                    self.no_match_df = self.no_match_df.append(imp_val_dict, \
                                                             ignore_index = True)
                    
                    self._update_trans(imp_val, 'impacted', 'no_match')

                    print len(self.no_match_df), len(self.impacted_df)   
        
        

#initialize model
mod_init = gs500(cnxn, isupply_table = 'workforce', sort_col = sort_col, \
                 impact_col = impact_col, sql_type='pyodbc', in_mem=in_mem, \
                 rules=rules)

#run model
##for period in xrange(1, periods + 1):
##    print "period: " + str(period)
##    print "Attrtion"
##    mod_init.attrit(period=period)
##    print "Closing Facilities"
##    mod_init.close_facs(period=period)
##    print "Move 1"
##    mod_init.move_people(dist_rest=dist_rest, hire=False, rule_en=[5])
##    # print "Move 2"
##    # mod_init.move_people(dist_rest=dist_rest, hire=False, rule_en=[1,2])
##    # print "Move 3"
##    # mod_init.move_people(dist_rest=dist_rest, hire=False, rule_en=[3])
##    # print "Move 4"
##    # mod_init.move_people(dist_rest=dist_rest, hire=True, rule_en=[4])
##    # print "Move 5"
##    # mod_init.move_people(dist_rest=dist_rest, hire=True, rule_en=[1,2])
##    # print "Move 6"
##    # mod_init.move_people(dist_rest=dist_rest, hire=True, rule_en=[3])
##    mod_init.update_summary(period=period)
