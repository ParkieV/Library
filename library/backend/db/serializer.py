from sqlalchemy import CursorResult
from typing import List
from datetime import datetime, date


def CursorResultDict(obj: CursorResult | List[CursorResult], *args, **kwargs) -> dict:
    if type(obj) is list:
        result_keys, result_items = [elem.keys() for elem in obj], [elem.items() for elem in obj]
        result_dict = []
        for i in range(len(result_keys)):
            result_dict.append(dict(zip(result_keys[i], result_items[i])))
        for i in range(len(result_dict)):
            for key in result_dict[i].keys():
                result_dict[i][key] = result_dict[i][key][1:]
                if len(result_dict[i][key]) == 1:
                    result_dict[i][key] = result_dict[i][key][0]
    else:
        result_keys, result_items = obj.keys(), obj.items()
        result_dict = dict(zip(result_keys, result_items))
        for key in result_dict.keys():
            result_dict[key] = result_dict[key][1:]
            if len(result_dict[key]) == 1:
                result_dict[key] = result_dict[key][0]
    return result_dict


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
