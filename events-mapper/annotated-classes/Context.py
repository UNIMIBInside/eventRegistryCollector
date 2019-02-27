# Since Context is defined as a static object, the following values are implemented
# as constants

VERSION = 1.1                   # @version
BASE = "http://ew-shopp.eu/"    # @base
SCHEMA = "http://schema.org/"   # schema
EWS = "http://schema.org/"      # ews (EW-Shopp ontology)
EWSR = "http://ew-shopp.eu/data/rdf"        # ewsr
XSD = "http://www.w3.org/2001/XMLSchema#"   # xsd
LANG = "@language"              # language
TEXT = "@value"                 # text
IDENTIFIER = "@id"              # identifier


class Context:
    def __init__(self):
        self._version = VERSION
        self._base = BASE
        self._schema = SCHEMA
        self._ews = EWS
        self._ewsr = EWSR
        self._lang = LANG
        self._text = TEXT
        self._identifier = IDENTIFIER
    
    def get_version(self):
        return self._version
    
    def get_base(self):
        return self._base
    
    def get_schema(self):
        return self._schema
    
    def get_ews(self):
        return self._ews
    
    def get_ewsr(self):
        return self._ewsr
    
    def get_lang(self):
        return self._lang
    
    def get_text(self):
        return self._text
    
    def get_identifier(self):
        return self._identifier