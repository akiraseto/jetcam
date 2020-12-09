import json

from util import request


class Data:
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
            print('Failed creating data port: ', res)
            exit()

    @classmethod
    def set_data_redirect(cls, data_connection_id, data_id, redirect_addr, redirect_port):
        """データの転送設定
        """

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
    def close_data_connections(cls, data_connection_id):
        """DataConnectionを開放する

        ----------
        :param data_connection_id: DataConnectionを特定するためのID
        :return: bool
        """

        res = request("delete", "/data/connections/{}".format(data_connection_id))
        if res.status_code == 204:
            print('release dataConnection')
            return True
        else:
            print('Failed closing dataConnection: ', res)
            return False
