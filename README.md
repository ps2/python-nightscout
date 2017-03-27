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

### Glucose Values
To fetch recent sensor glucose values (SGVs):

	entries = api.get_sgvs()
	print([entry.sgv for entry in entries])

Specify time ranges:

	api.get_sgvs({'count':0, 'find[dateString][$gte]': '2017-03-07T01:10:26.000Z'})

### Treatments
To fetch recent treatments (boluses, temp basals):

	treatments = api.get_treatments()
	print([treatment.eventType for treatment in treatments])

### Profiles

	profile_definition_set = api.get_profiles()

	profile_definition = profile_definition_set.get_profile_definition_active_during(datetime.now())

	profile = profile_definition.get_default_profile()
        
	print "Duration of insulin action = %d" % profile.dia
	
	five_thirty_pm = datetime(2017, 3, 24, 17, 30)
	five_thirty_pm = profile.timezone.localize(five_thirty_pm)
	print "Scheduled basal rate at 5:30pm is = %f" % profile.basal.value_at_time(five_thirty_pm)

