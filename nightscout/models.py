import dateutil.parser

class SGV(object):
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
    def new_from_json_dict(cls, data, **kwargs):
        json_data = data.copy()
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val

        if json_data['dateString']:
            json_data['date'] = dateutil.parser.parse(json_data['dateString'])

        c = cls(**json_data)
        c._json = data
        return c
