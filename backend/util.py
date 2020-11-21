import json
import requests
import asyncio

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
    elif method_name == 'post':
        response = requests.post(uri, *args)
    elif method_name == 'put':
        response = requests.put(uri, *args)
    elif method_name == 'delete':
        response = requests.delete(uri)

    else:
        print('There is no method called it')

    return response


def async_get_event(uri, event):
    # todo:SubThreadで実装する
    e = None

    while e is None or e["event"] != event:
        res = request('get', uri)

        if res.status_code == 200:
            e = json.loads(res.text)

    return e


async def listen_event(event, peer_id, peer_token, loop=None):
    """イベントを待ち受ける
    """

    print('start listen_event:', event)
    url = "/peers/{}/events?token={}".format(peer_id, peer_token)

    if event == 'CALL':
        res = await loop.run_in_executor(None, async_get_event, url, "CALL")
        print('end listen_call_event')
        return res["call_params"]["media_connection_id"]

    elif event == 'CONNECTION':
        res = await loop.run_in_executor(None, async_get_event, url, "CONNECTION")
        print('end listen_connect_event')
        return res["data_params"]["data_connection_id"]

    # elif event == 'OPEN':
    #     res = async_get_event(url, "OPEN")
    #     # res = await loop.run_in_executor(None, async_get_event, url, "OPEN")
    #     return res["params"]["peer_id"], res["params"]["token"]

    else:
        print('event is wrong')
