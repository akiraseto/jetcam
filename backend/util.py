import json
import requests
import socket


def request(method_name, uri, *args):
    response = None
    if method_name == 'get':
        response = requests.get(uri, *args)
    elif method_name ==  'post':
        response = requests.post(uri, *args)
    elif method_name ==  'put':
        response = requests.put(uri, *args)
    else:
        print('There is no method called it')

    return response

def async_get_event(uri, event):
    # 非同期処理
    e = None

    while e == None or e["event"] != event:
        res = request('get', uri)

        e = json.dumps(res.body)


