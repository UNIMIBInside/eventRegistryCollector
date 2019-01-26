from eventregistry import *
import eventregistry as ER
import argparse

def init_connection_er(access_token):
    if access_token is not None:
        er = ER.EventRegistry(access_token)
    else:
        raise Exception("ERROR: No access_token has been specified")
    
    return er

def get_events_by_location(access_token, location):
    # establishing connection with Event Register
    er = init_connection_er(access_token)

    # set query to get events
    q = QueryEvents(
        sourceLocationUri = er.getLocationUri(location)
    )

    # keep just the first 2000 results
    q.setRequestedResult(ER.RequestEventsInfo(count=2000))

    # exec query
    res = er.execQuery(q)

if __name__ == "__main__":

    # command-line argument parser declaration
    parser = argparse.ArgumentParser()

    # add argument that require access token
    parser.add_argument('-a', '--access_token', default=None, help="Event Registry API access token")

    # add argument that require location to look for events
    parser.add_argument('-l', '--location', type= str, default=None, help="Location to look for events")

    args = parser.parse_args()

    if args.location:
        get_events_by_location(args.access_token, args.location)