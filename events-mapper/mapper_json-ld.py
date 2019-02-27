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
data_out['@context'] = {
    "@version": context.get_version(),
    "@base": context.get_base(),
    "schema": context.get_schema(),
    "ews": context.get_ews(),
    "ewsr": context.get_ewsr(),
    "lang": context.get_lang(),
    "text": context.get_text(),
    "identifier": context.get_identifier(),
    "eventArray": context.get_eventArray(),
    "name": context.get_name(),
    "description": context.get_description(),
    "source": context.get_source(),
    "channelCode": context.get_channelCode(),
    "channelDescription": context.get_channelDescr(),
    "startDate": context.get_startDate(),
    "endDate": context.get_endDate(),
    "category": context.get_category(),
    "product": context.get_product(),
    "gtin13": context.get_gtin13(),
    "seller": context.get_seller(),
    "sku": context.get_sku(),
    "catalogId": context.get_catalogId(),
    "measure": context.get_measure(),
    "quantity": context.get_quantity(),
    "quantityUnitId": context.get_quantityUnitId(),
    "interestedAudience": context.get_interestedAudience(),
    "attendingAudience": context.get_attendingAudience(),
    "priceChanged": context.get_priceChanged(),
    "discount": context.get_discount(),
    "location": context.get_location(),
    "addressLocality": context.get_addressLocality(),
    "addressCountry": context.get_addressCountry(),
    "addressRegion": context.get_addressRegion(),
    "streetAddress": context.get_streetAddress(),
    "postalCode": context.get_postalCode(),
    "latitude": context.get_latitude(),
    "longitude": context.get_longitude(),
    "address": context.get_address()
}

pprint(data_out)

# EVENTS
events_arr_in = data_in["events"]["results"]

# Building output json file
data_out['events'] = []

for event in events_arr_in:
    curr_event = evnt.Event(event)
    data_out['events'].append(
        {
            "@type": curr_event.get_type(),
            "identifier": curr_event.get_identifier(),
            "name": curr_event.get_name(),
            "description": curr_event.get_description(),
            "location": {
                "@type": curr_event.get_location().get_type(),
                "name": curr_event.get_location().get_name(),
                "latitude": curr_event.get_location().get_latitude(),
                "longitude": curr_event.get_location().get_longitude()
            }
        }
    )

# Dump data_out dictionary in a JSON output file
with open('data_mapped.json','w') as outfile:
    json.dump(data_out, outfile, indent=4)
    outfile.write("\n")