import json
import socket

from util import *


class Data():
    """DataChannelを利用する

    DataConnectionオブジェクトと転送するデータの送受信方法について指定
    """

    @classmethod
    def create_data(cls):
        """Dataの待受ポート開放要求を送信

        ----------
        :return: data_id, port
        """
        res = request("post", "/data", "{}")
        if res.status_code == 201:
            json_text = json.loads(res.text)
            data_id = json_text["data_id"]
            ip_v4 = json_text["ip_v4"]
            port = json_text["port"]

            return data_id, ip_v4, port

        else:
            print(res)
            exit()


    @classmethod
    def listen_connect_event(cls, peer_id, peer_token):
        # todo:非同期で実装
        e = async_get_event("/peers/{}/events?token={}".format(peer_id, peer_token), "CONNECTION")
        data_connection_id = e["data_params"]["data_connection_id"]

        return data_connection_id

    @classmethod
    def set_data_redirect(cls, data_connection_id, data_id, redirect_addr, redirect_port):
        params = {
            # for sending data
            "feed_params": {
                "data_id": data_id,
            },
            # for receiving data
            "redirect_params": {
                "ip_v4": redirect_addr,
                "port": redirect_port,
            },
        }

        res = request("put", "/data/connections/{}".format(data_connection_id), json.dumps(params))
        print(res)


    @classmethod
    def close_data(cls, data_connection_id):
        """Dataの待受ポートの閉鎖要求を送信

        ----------
        :param data_connection_id: Dataを特定するためのID
        :return: None(正常終了)
        """
        res = request("delete", "/data/connections/{}".format(data_connection_id))
        if res.status_code == 204:
            print('close data')
            return None
        else:
            print(res)
            exit()







