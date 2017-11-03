from flask.json import JSONEncoder
from datetime import datetime

class JSONDateEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                #"2017-01-25T09:05:14.309-02:00"
                return obj.replace().strftime('%Y-%m-%d %H:%M:%S')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

def parseAdiTag(aditag):
    aditag = aditag.replace('(','',1).strip(' ')
    elem = aditag.partition(')')
    return {
        'type':elem[0],
        'tag':elem[2]
    }
