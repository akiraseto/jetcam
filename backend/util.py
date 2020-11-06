import json
import requests

from config import *


def request(method_name, _uri, *args):
    """gatewayにAPIリクエストする

    ----------
    :param method_name: REST APIメソッド
    :param _uri: リクエスト先のURI
    :param args: 主にjson payload
    :return: gatewayからのレスポンス
    """
    response = None
    uri = HOST + _uri
    if method_name == 'get':
        response = requests.get(uri, *args)
    elif method_name ==  'post':
        response = requests.post(uri, *args)
    elif method_name ==  'put':
        response = requests.put(uri, *args)
    elif method_name ==  'delete':
        response = requests.delete(uri)

    else:
        print('There is no method called it')

    return response


def async_get_event(uri, event):
    # todo:非同期処理で実装する
    e = None

    while e is None or e["event"] != event:
        res = request('get', uri)

        if res.status_code == 200:
            e = json.loads(res.text)

    return e
