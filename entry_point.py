import argparse
import os
import configparser
import re
from pprint import pprint

from src.collector import eventregistry_collector as ercoll
from src.db_connector import arangodb_connector as arandb

# Get available collector services
def get_avail_coll_services(cfg):
    """
    Extract fields from ini file about available collectors
    """
    coll_services = {}
    i = 1

    for section in cfg.sections():
        if 'collector' in section:
            coll_services[str(i)] = {
                "name": section.split('.',1)[1],
                "section": section,
                "accesstoken": cfg[section]["accesstoken"],
            }

            i += 1
    
    return coll_services

def get_avail_db_conn(cfg):
    """
    Extract fields from ini file about available db connectors
    """
    conn_db = {}
    i = 1

    for section in cfg.sections():
        if 'db.connector.' in section:

            conn_db[str(i)] = {
                "name": section.split('.',1)[1],
                "section": section,
                "port": cfg[section]["port"],
                "user": cfg[section]["user"],
                "password": cfg[section]["password"],
                "db_name": cfg[section]["db_name"]
            }

            if cfg[section]["specificIPmode"] == 'yes':
                conn_db[str(i)]["IP"] = cfg[section]["IP"]
            else:
                conn_db[str(i)]["IP"] = cfg["db.connector"]["IP"]
            
            if "coll_name" in cfg[section]:
                conn_db[str(i)]["coll_name"] = cfg[section]["coll_name"]
            else:
                conn_db[str(i)]["table_name"] = cfg[section]["table_name"]

            
            i += 1
    
    return conn_db

def coll_service_selection(avail_coll_services):
    """
    Let the user choose the service to which perform the query
    """ 
    print("Please, select collector service (type related number key):")
    
    for coll_serv_key in avail_coll_services:
        print("[" + coll_serv_key + "] " + avail_coll_services[coll_serv_key]["name"]) # fare a dizionario e fare check sulle chiavi disponibili

    coll_valid = False
    selected_collector = ""

    while not coll_valid:
        
        print("Your selection:", end=" ")
        selected_collector = input()
        if selected_collector not in avail_coll_services:
            print("[Error] Your choice does not correspond to any of the available services, retry")
        else:
            coll_valid = True
    
    return avail_coll_services[selected_collector]

# Events collection
def collect_from_service(selected_collector):
    """
    Query services to get events and collect results in a JSON file
    """

    # TODO: Way to do this in a non-hardcoded way?
    collector_cstr = {
        "eventregistry": ercoll.ERCollector,
    }

    accesstoken = selected_collector["accesstoken"]
    collector = collector_cstr[selected_collector["name"]](accesstoken)

    # ER query filtering
    filters = {}
    print("\nSpecify filtering, leave blank if you do not want set a filter")
    print("Location:", end=" ")
    
    # Filter location
    filters["location"] = input()

    # Filter event date
    date_start_valid = False
    date_end_valid = False

    # TODO: IMPORTANT! Add dateStart and dateEnd
    while not (date_start_valid & date_end_valid):
        print("Event start date (yyyy-MM-dd):", end=" ")
        filters["startDate"] = input()
       
        pattern_date = re.compile("(^$|^\d{4}(-)(((0)[0-9])|((1)[0-2]))(-)([0-2][0-9]|(3)[0-1])$)")
        match_start_date = pattern_date.match(filters["startDate"])

        if match_start_date is not None:
            date_start_valid = True
        else:
            print("[ERROR] Input date invalid or format not recognized")


        print("Event end date (yyyy-MM-dd):", end=" ")
        filters["endDate"] = input()
       
        match_end_date = pattern_date.match(filters["endDate"])

        if match_end_date is not None:
            date_end_valid = True
        else:
            print("[ERROR] Input date invalid or format not recognized")

    for filter in filters:
        if filters[filter] == '':
            filters[filter] = None

    collector.exec_query(filters)

def conn_db_selection(avail_db_conn):
    """
    Let the user choose the db connector to interface with db engine
    """
        
    print("Please, select collector service (type related number key):")
    
    for conn_db_key in avail_db_conn:
        print("[" + conn_db_key + "] " + avail_db_conn[conn_db_key]["name"]) # fare a dizionario e fare check sulle chiavi disponibili

    conn_db_valid = False
    selected_conn_db = ""
    
    while not conn_db_valid:
        print("Your selection:", end=" ")
        selected_conn_db = input()
        if selected_conn_db not in avail_db_conn:
            print("[Error] Your choice does not correspond to any of the available connectors, retry")
        else:
            conn_db_valid = True
    
    return avail_db_conn[selected_conn_db]


# Map events into JSON-LD
def map_to_jsonld():
    """
    Map the query resulting JSON file into JSON-LD according to the custom ontology
    """
    os.system("py src/mapper/mapper_json_ld.py")

# Save events into db
def save_events(selected_db_conn):
    """
    Save a JSON-LD file containing events got from a service into a DB instance
    """
    # TODO: Way to do this in a non-hardcoded way?
    conn_db_cstr = {
        "connector.arangodb": arandb.ArangoDBConnector,
    }

    conn_ip = selected_db_conn["IP"]  # extract IP from ini file
    conn_port = selected_db_conn["port"]    # extract port from ini file
    conn_user = selected_db_conn["user"]
    conn_password = selected_db_conn["password"]
    conn_db_name = selected_db_conn["db_name"]
    conn_table_coll_name = ""

    if "coll_name" in selected_db_conn:
        conn_table_coll_name = selected_db_conn["coll_name"]
    else:
        conn_table_coll_name = selected_db_conn["table_name"]

    print(selected_db_conn["name"])
    conn_db = conn_db_cstr[selected_db_conn["name"]](conn_ip,conn_port,'http',conn_user,conn_password) # call the specified constructor
    db = conn_db.connect(conn_db_name,conn_table_coll_name)
    conn_db.save_all(db)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # add argument to choose the mode: only events donwload, only mapping, both
    parser.add_argument('-m','--mode', type=str, default='dm', 
        help="['d' download events | 'm' map events | 'dm' do both] (Default 'dm')")     

    args = parser.parse_args()

    # read config file
    cfg = configparser.ConfigParser()
    cfg.read('config/config.ini')

    if (args.mode == 'd') | (args.mode == 'dm'):
        # init available collector services
        avail_coll_services = get_avail_coll_services(cfg)

        selected_collector = coll_service_selection(avail_coll_services)
        collect_from_service(selected_collector)
    
    if (args.mode == 'm') | (args.mode == 'dm'):
        map_to_jsonld()

        # init available db connectors
        avail_db_conn = get_avail_db_conn(cfg)

        selected_db_conn = conn_db_selection(avail_db_conn)
        pprint(selected_db_conn)
        save_events(selected_db_conn)