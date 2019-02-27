import PostalAddress as pa

TYPE = "ews:place"

class Place:
    def __init__(self,er_event):
        self._type = TYPE
        self._name = er_event["location"]["label"]["eng"]
        # self._description 
        self._latitude = er_event["location"]["lat"]
        self._longitude = er_event["location"]["long"]
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