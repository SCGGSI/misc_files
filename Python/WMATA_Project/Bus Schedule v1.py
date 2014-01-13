# Imports

from urllib import urlopen
from datetime import datetime as DT
import xml.etree.ElementTree as ET

# Constants

web_site = "http://api.wmata.com/Bus.svc/RouteSchedule?routeId=%s&date=2013-07-05&includingVariations=true&api_key=z3k93zgdm7t5cyaf7n4b72b7"
bus_list = ['11Y', '13F', '13G', '16X', '16Y', '31', '32', '34', '36', '37', \
            '38B', '39', '3Y', '42', '43', '52', '53', '54', '5A', '63', \
            '64', '70', '74 NOR', '74 SOU', '79', '7Y', '80', '96', 'A11', \
            'A42', 'A46', 'A48', 'A9', 'D1', 'D3', 'D4', 'D5', 'D6', 'D8', \
            'G8', 'H1', 'L1', 'L2', 'N2', 'N3', 'N4', 'N6', 'P17', 'P19', \
            'P6', 'S1', 'S2', 'S4', 'S9', 'V5', 'V7', 'V8', 'V9', 'W13', 'X1', \
            'X2', 'X9']

start_1 = DT(2013, 7, 3, 7, 0, 0)
stop_1 = DT(2013, 7, 3, 9, 30, 0)
start_2 = DT(2013, 7, 3, 16, 0, 0)
stop_2 = DT(2013, 7, 3, 18, 30, 0)

# Functions

def bus_stops(bus):
    w_hnd = urlopen(web_site % bus)
    xml_text = w_hnd.readlines()
    root = ET.fromstring(''.join(xml_text))
    
    for direction in root:
        for trip in direction:
            for stop in trip[4]:

                temp_time = stop[3].text.split('T')[1].split(':')
                stop_time = DT(2013, 7, 3, int(temp_time[0]), \
                    int(temp_time[1]), int(temp_time[2]))

                if start_1 <= stop_time <= stop_1 or \
                start_2 <= stop_time <= stop_2:
                    stop_ids.append((bus, stop[0].text, stop[1].text, \
                                     stop_time))

    
            
# Main

if __name__ == "__main__":
    stop_ids = []  
    for i, bus in enumerate(bus_list):
        print i, bus
        try:
            bus_stops(bus)

        except:

            print "Error with bus %s. Trying again." % bus
            try:
                bus_stops(bus)

            except:
                print "Trying one more time."
                bus_stops(bus)
        
		
