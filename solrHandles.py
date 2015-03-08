from mysolr import Solr
import requests

# set connection through requests
session = requests.Session()
solr_handle = Solr('http://localhost/solr4/autocomplete', make_request=session)
