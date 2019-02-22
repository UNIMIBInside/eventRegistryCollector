from eventregistry import *
import eventregistry as ER
import argparse
import json

def init_connection_er(access_token):
    """
    Establish connection with EventRegistry service
    """
    if access_token is not None:
        er = ER.EventRegistry(access_token)
    else:
        raise Exception("ERROR: No access_token has been specified")
    
    return er

def get_events_by_location(access_token, location):
    # establishing connection with Event Register
    er = init_connection_er(access_token)

    print(type(location))

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
                geoLocation = True  # return geographic coordinates of the place/country
        ))
    ))

    # exec query
    res = er.execQuery(q)

    # dump result on a JSON file
    with open('data.json', 'w') as outfile:
        json.dump(res, outfile)


if __name__ == "__main__":

    # command-line argument parser declaration
    parser = argparse.ArgumentParser()

    # add argument that require access token
    parser.add_argument('-a', '--access_token', type=str, default=None, help="Event Registry API key")

    # add argument that require location to look for events
    parser.add_argument('-l', '--location', type= str, default=None, help="Filter events on location")

    args = parser.parse_args()

    print(args.location)

    if args.location:
        get_events_by_location(args.access_token, args.location)