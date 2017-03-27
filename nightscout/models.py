import dateutil.parser
import pytz

class BaseModel(object):
    def __init__(self, **kwargs):
        self.param_defaults = {}

    @classmethod
    def json_transforms(cls, json_data):
        pass

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        json_data = data.copy()
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val

        cls.json_transforms(json_data)

        c = cls(**json_data)
        c._json = data
        return c


class SGV(BaseModel):
    """Sensor Glucose Value

    Represents a single glucose measurement and direction at a specific time.

    Attributes:
        sgv (int): Glucose measurement value in mg/dl.
        date (datetime): The time of the measurement
        direction (string): One of ['DoubleUp', 'SingleUp', 'FortyFiveUp', 'Flat', 'FortyFiveDown', 'SingleDown', 'DoubleDown']
        device (string): the source of the measurement.  For example, 'share2', if pulled from Dexcom Share servers
    """
    def __init__(self, **kwargs):
        self.param_defaults = {
            'sgv': None,
            'date': None,
            'direction': None,
            'device': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    @classmethod
    def json_transforms(cls, json_data):
        if json_data.get('dateString'):
            json_data['date'] = dateutil.parser.parse(json_data['dateString'])


class Treatment(BaseModel):
    """Nightscout Treatment

    Represents an entry in the Nightscout treatments store, such as boluses, carb entries,
    temp basals, etc. Many of the following attributes will be set to None, depending on
    the type of entry.

    Attributes:
        eventType (string): The event type. Examples: ['Temp Basal', 'Correction Bolus', 'Meal Bolus', 'BG Check']
        timestamp (datetime): The time of the treatment
        insulin (float): The amount of insulin delivered
        programmed (float): The amount of insulin programmed. May differ from insulin if the pump was suspended before delivery was finished.
        carbs (int): Amount of carbohydrates in grams consumed
        rate (float): Rate of insulin delivery for a temp basal, in U/hr.
        duration (int): Duration in minutes for a temp basal.
        enteredBy (string): The person who gave the treatment if entered in Care Portal, or the device that fetched the treatment from the pump.
        glucose (int): Glucose value for a BG check, in mg/dl.
    """
    def __init__(self, **kwargs):
        self.param_defaults = {
            'temp': None,
            'enteredBy': None,
            'eventType': None,
            'glucose': None,
            'glucoseType': None,
            'units': None,
            'device': None,
            'created_at': None,
            'timestamp': None,
            'absolute': None,
            'rate': None,
            'duration': None,
            'carbs': None,
            'insulin': None,
            'unabsorbed': None,
            'suspended': None,
            'type': None,
            'programmed': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    @classmethod
    def json_transforms(cls, json_data):
        if json_data.get('timestamp'):
            json_data['timestamp'] = dateutil.parser.parse(json_data['timestamp'])
        if json_data.get('created_at'):
            json_data['created_at'] = dateutil.parser.parse(json_data['created_at'])


class ScheduleEntry(BaseModel):
    """ScheduleEntry

    Represents an entry in one of the schedules on a Nightscout profile.

    Attributes:
        value (double): The value of the entry. Interpetation depends on the type of schedule this entry is on.
        timeAsSeconds (int): The start time of the entry, in seconds since midnight
    """
    def __init__(self, **kwargs):
        self.param_defaults = {
            'time': None,
            'value': None,
            'timeAsSeconds': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    @classmethod
    def json_transforms(cls, json_data):
        if json_data.get('value'):
            json_data['value'] = float(json_data['value'])
        if json_data.get('timeAsSeconds'):
            json_data['timeAsSeconds'] = int(json_data['timeAsSeconds'])


class Schedule(object):
    """ScheduleEntry

    Represents a schedule on a Nightscout profile.

    """
    def __init__(self, entries):
        self.entries = entries
        self.entries.sort(key=lambda e: e.timeAsSeconds)

    # Expects a localized timestamp here
    def value_at_time(self, local_time):
        """Get scheduled value at given time

        Args:
            local_time: The time of interest. It should be a localized time.

        Returns:
            The value of the schedule at the given time. Interpetation depends on the type of schedule.

        """
        seconds_offset = (local_time - local_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        return [e.value for e in self.entries if e.timeAsSeconds <= seconds_offset][-1]

    @classmethod
    def new_from_json_array(cls, data):
        entries = [ScheduleEntry.new_from_json_dict(d) for d in data]
        return cls(entries)


class Profile(BaseModel):
    """Profile

    Represents a Nightscout profile.

    Attributes:
        dia (double): The duration of insulin action, in hours.
        carb_ratio (Schedule): A schedule of carb ratios, which are in grams/U.
        sens (Schedule): A schedule of insulin sensitivity values, which are in mg/dl/U.
        timezone (timezone): The timezone of the schedule.
        basal (Schedule): A schedule of basal rates, which are in U/hr.
        target_low (Schedule): A schedule the low end of the target range, in mg/dl.
        target_high (Schedule): A schedule the high end of the target range, in mg/dl.
    """
    def __init__(self, **kwargs):
        self.param_defaults = {
            'dia': None,
            'carb_ratio': None,
            'carbs_hr': None,
            'delay': None,
            'sens': None,
            'timezone': None,
            'basal': None,
            'target_low': None,
            'target_high': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    @classmethod
    def json_transforms(cls, json_data):
        if json_data.get('timezone'):
            json_data['timezone'] = pytz.timezone(json_data.get('timezone'))
        if json_data.get('carbratio'):
            json_data['carbratio'] = Schedule.new_from_json_array(json_data.get('carbratio'))
        if json_data.get('sens'):
            json_data['sens'] = Schedule.new_from_json_array(json_data.get('sens'))
        if json_data.get('target_low'):
            json_data['target_low'] = Schedule.new_from_json_array(json_data.get('target_low'))
        if json_data.get('target_high'):
            json_data['target_high'] = Schedule.new_from_json_array(json_data.get('target_high'))
        if json_data.get('basal'):
            json_data['basal'] = Schedule.new_from_json_array(json_data.get('basal'))
        if json_data.get('dia'):
            json_data['dia'] = int(json_data['dia'])

class ProfileDefinition(BaseModel):
    """ProfileDefinition

    Represents a Nightscout profile definition, which can have multiple named profiles.

    Attributes:
        startDate (datetime): The time these profiles start at.
    """
    def __init__(self, **kwargs):
        self.param_defaults = {
            'defaultProfile': None,
            'store': None,
            'startDate': None,
            'created_at': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def get_default_profile(self):
        return self.store[self.defaultProfile]

    @classmethod
    def json_transforms(cls, json_data):
        if json_data.get('startDate'):
            json_data['startDate'] = dateutil.parser.parse(json_data['startDate'])
        if json_data.get('created_at'):
            json_data['created_at'] = dateutil.parser.parse(json_data['created_at'])
        if json_data.get('store'):
            store = {}
            for profile_name in json_data['store']:
                store[profile_name] = Profile.new_from_json_dict(json_data['store'][profile_name])
            json_data['store'] = store

class ProfileDefinitionSet(object):
    """ProfileDefinitionSet

    Represents a set of Nightscout profile definitions, each covering a range of time
    from its start time, to the start time of the next profile definition, or until
    now if there are no newer profile defitions.

    """
    def __init__(self, profile_definitions):
        self.profile_definitions = profile_definitions
        self.profile_definitions.sort(key=lambda d: d.startDate)

    def get_profile_definition_active_during(self, date):
        """Get the profile definition active at a given datetime

        Args:
            date: The profile definition containing this time will be returned.

        Returns:
            A ProfileDefinition object valid for the specified time.

        """
        return [d for d in self.profile_definitions if d.startDate <= date][-1]

    @classmethod
    def new_from_json_array(cls, data):
        defs = [ProfileDefinition.new_from_json_dict(d) for d in data]
        return cls(defs)
