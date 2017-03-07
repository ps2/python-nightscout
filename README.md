# Python Nightscout client

[![Build Status](https://travis-ci.org/ps2/python-nightscout.svg?branch=master)](https://travis-ci.org/ps2/python-nightscout)

A simple python client for accessing data stored in [Nightscout](https://github.com/nightscout/cgm-remote-monitor)

## Example Usage

To create an instance of the nightscout.Api class, with no authentication:

	import nightscout
    api = nightscout.Api('https://yournightscoutsite.herokuapp.com')

To use authentication, instantiate the nightscout.Api class with your
    api secret:

	api = nightscout.Api('https://yournightscoutsite.herokuapp.com', api_secret='your api secret')

To fetch recent sensor glucose values (SGVs):

	entries = api.get_sgvs()
	print([entry.sgv for entry in entries])
