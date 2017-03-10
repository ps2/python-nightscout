import dateutil.parser

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
    def __init__(self, **kwargs):
        self.param_defaults = {
            'temp': None,
            'enteredBy': None,
            'eventType': None,
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
    def __init__(self, **kwargs):
        self.param_defaults = {
            'time': None,
            'value': None,
            'timeAsSeconds': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))


class Profile(BaseModel):
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
            'startDate': None,
            'units': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    @classmethod
    def json_transforms(cls, json_data):
        if json_data.get('startDate'):
            json_data['startDate'] = dateutil.parser.parse(json_data['startDate'])
        if json_data.get('carbratio'):
            json_data['carbratio'] = [ScheduleEntry.new_from_json_dict(x) for x in json_data.get('carbratio')]
        if json_data.get('sens'):
            json_data['sens'] = [ScheduleEntry.new_from_json_dict(x) for x in json_data.get('sens')]
        if json_data.get('target_low'):
            json_data['target_low'] = [ScheduleEntry.new_from_json_dict(x) for x in json_data.get('target_low')]
        if json_data.get('target_high'):
            json_data['target_high'] = [ScheduleEntry.new_from_json_dict(x) for x in json_data.get('target_high')]

class ProfileRecord(BaseModel):
    def __init__(self, **kwargs):
        self.param_defaults = {
            'defaultProfile': None,
            'store': None,
            'startDate': None,
            'units': None,
            'created_at': None,
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

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
