import PostalAddress as pa

TYPE = "ews:place"

class Place:
    def __init__(self,er_event_location):
        self._type = TYPE
        self._name = er_event_location["label"]["eng"]
        # self._description 
        self._latitude = er_event_location["lat"]
        self._longitude = er_event_location["long"]
        #self._address = pa.PostalAddress()
    
    def get_type(self):
        return self._type
    
    def get_name(self):
        return self._name
    
    def get_latitude(self):
        return self._latitude
    
    def get_longitude(self):
        return self._longitude
    
    def get_address(self): ###
        return self._address