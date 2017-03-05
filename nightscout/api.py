"""A library that provides a Python interface to Nightscout"""
import requests
import hashlib
from nightscout import (
    SGV,
)

class Api(object):
    """A python interface into Nightscout

    Example usage:
      To create an instance of the nightscout.Api class, with no authentication:
        >>> import nightscout
        >>> api = nightscout.Api('https://yournightscoutsite.herokuapp.com')
      To use authentication, instantiate the nightscout.Api class with your
      api secret:
        >>> api = nightscout.Api('https://yournightscoutsite.herokuapp.com', api_secret='your api secret')
      To fetch recent sensor glucose values (SGVs):
        >>> entries = api.get_sgvs()
        >>> print([entry.sgv for entry in entries])
    """

    def __init__(self, site_url, api_secret=None):
        """Instantiate a new nightscout.Api object."""
        self.site_url = site_url
        self.api_secret = api_secret

    def request_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.api_secret:
            headers['api-secret'] = hashlib.sha1(self.api_secret).hexdigest()
        return headers

    def get_sgvs(self):
        r = requests.get(self.site_url + '/api/v1/entries/sgv.json', headers=self.request_headers())
        return [SGV.new_from_json_dict(x) for x in r.json()]
