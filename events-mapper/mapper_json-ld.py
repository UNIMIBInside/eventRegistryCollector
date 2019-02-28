import json
from pprint import pprint   # TODO: to be removed

import sys
sys.path.append('./annotated-classes/')
import Event as evnt
import Context as cntxt
import Place as plc


# Data from input json file
data_in = {}

# Data resulting after parsing
data_out = {}

# Read and load in a local variable input json file content
with open('../data.json') as f:
    data_in = json.load(f)

# CONTEXT
context = cntxt.Context()

# Bulding output json file
data_out['@context'] = context.repr()

# EVENTS
events_arr_in = data_in["events"]["results"]

# Building output json file
data_out['events'] = []

for event in events_arr_in:
    curr_event = evnt.Event(event)
    data_out['events'].append(curr_event.repr())

# Dump data_out dictionary in a JSON output file
with open('data_mapped.json','w') as outfile:
    json.dump(data_out, outfile, indent=4)
    outfile.write("\n")