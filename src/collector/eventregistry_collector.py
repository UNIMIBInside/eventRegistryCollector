from eventregistry import *
import eventregistry as ER
import argparse
import json
import re

from .icollector import Collector

from pprint import pprint

class ERCollector(Collector):

    def __init__(self, access_token = None):
        self._access_token = access_token
        self._er = None

        super(Collector, self).__init__()
    
    def connect_to_service(self):
        """
        Establish connection with EventRegistry service
        """
        if self._access_token is not None:
            self._er = ER.EventRegistry(self._access_token)
        else:
            raise Exception("[ERROR] No access_token has been specified")
        
        return self._er
    
    def exec_query(self, filters = None):
        
        er = self.connect_to_service()

        # set query to get events
        q = QueryEvents(
            locationUri = er.getLocationUri(filters["location"]),
            dateStart = filters["startDate"],
            dateEnd = filters["endDate"] 
        )

        # keep just the first 2000 results
        q.setRequestedResult(
            ER.RequestEventsInfo(
                count=50,
                sortBy = "eventDate", 
                sortByAsc = False,
                returnInfo = ReturnInfo(locationInfo = LocationInfoFlags(
                    wikiUri = True,     # return wiki url og the place/country
                    countryDetails = True,  # return details about country
                    geoLocation = True  # return geographic coordinates of the place/country
            ))
        ))

        # exec query
        res = er.execQuery(q)

        # dump result on a JSON file
        with open('data.json', 'w') as outfile:
            json.dump(res, outfile)
        
        # TODO: remove the following code in this function after test activity
        elem = res["events"]["results"][0]
        del elem["concepts"]

        with open('data_elem.json','w') as outfile:
            json.dump(elem, outfile)

'''
def get_events_by_location(access_token):

    # establishing connection with Event Register
    er = init_connection_er(access_token)

    

    # set query to get events
    q = QueryEvents(
        locationUri = er.getLocationUri(filters["location"])
    )

    # keep just the first 2000 results
    q.setRequestedResult(
        ER.RequestEventsInfo(
            count=50,
            sortBy = "eventDate", 
            sortByAsc = False,
            returnInfo = ReturnInfo(locationInfo = LocationInfoFlags(
                wikiUri = True,     # return wiki url og the place/country
                countryDetails = True,  # return details about country
                geoLocation = True  # return geographic coordinates of the place/country
        ))
    ))

    # exec query
    res = er.execQuery(q)

    # dump result on a JSON file
    with open('data.json', 'w') as outfile:
        json.dump(res, outfile)
    
    # TODO: remove the following code in this function after test activity
    elem = res["events"]["results"][0]
    del elem["concepts"]

    with open('data_elem.json','w') as outfile:
        json.dump(elem, outfile)

if __name__ == "__main__":

    print("---- ER Collector ---")

    # ER API key input request
    print("Please, specify EventRegistry API Key:", end=' ')
    er_api_key = input()
   
    get_events_by_location(er_api_key)
'''