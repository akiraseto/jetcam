import json
import requests


def request(method_name, uri, *args):
    if method_name == 'get':
        response = requests.get(uri, *args)
    elif method_name ==  'post':
        response = requests.post(uri, *args)
    elif method_name ==  'put':
        response = requests.put(uri, *args)
    else:
        print('There is no method called it')

def async_get_event(uri, event):
    e = None

    while e == None or e["event"] != event:
        res = request('get', uri)

        e = json.dumps(res.body)



