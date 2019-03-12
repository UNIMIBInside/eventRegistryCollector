from eventregistry import *
import eventregistry as ER
import argparse
import json
import re

def init_connection_er(access_token):
    """
    Establish connection with EventRegistry service
    """
    if access_token is not None:
        er = ER.EventRegistry(access_token)
    else:
        raise Exception("[ERROR] No access_token has been specified")
    
    return er

def get_events_by_location(access_token):

    # establishing connection with Event Register
    er = init_connection_er(access_token)

    # ER query filtering
    filters = {}
    print("\nSpecify filtering, leave blank if you do not want set a filter")
    print("Location:", end=" ")
    
    # Filter location
    filters["location"] = input()

    # Filter event date
    date_valid = False

    while not date_valid:
        print("Event date (yyyy-MM-dd):", end=" ")
        filters["eventDate"] = input()
    
        pattern_date = re.compile("([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))")
        match_date = pattern_date.match(filters["eventDate"])

        if match_date is not None:
            date_valid = True
        else:
            print("[ERROR] Date invalid or input date format is not recognized")

    # set query to get events
    q = QueryEvents(
        locationUri = er.getLocationUri(location)
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