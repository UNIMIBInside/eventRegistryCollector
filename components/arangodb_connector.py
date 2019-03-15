from arango import ArangoClient
from pprint import pprint
import json

db = None

def estrablish_conn():
    client = ArangoClient(protocol='http', host='192.168.99.100', port=8529)
    sys_db = client.db('_system', username='root', password='')

    # create db if not exists
    if not sys_db.has_database('events'):
        sys_db.create_database('events')

    # establish connection with db
    db = client.db('events', username='root', password='')

    # create collection if not exists
    if not db.has_collection('events_coll'):
        evnt_coll = db.create_collection('events_coll')

    return db

def process_evnts(db):

    events = []
    coll = db.collection("events_coll")

    with open('./data_mapped.json') as f:
        data_in = json.load(f)
        events = data_in["events"]

    for event in events:
        e = event
        e["_id"] = e.pop("identifier")
        e["_id"] = coll.name + "/" + str(e["_id"])

        # save event as a ArangoDB document
        if not db.has_document(e):
            db.insert_document('events_coll', e)

if __name__ == "__main__":
    
    print("---- ArangoDB connector ---")

    # init connection with ArangoDB instance
    db = estrablish_conn()

    # process JSON-LD containing events
    process_evnts(db)

    print("[INFO] Events file loading on ArangoDB database has been completed")