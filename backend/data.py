from util import *


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
    async def listen_connect_event(cls, peer_id, peer_token, loop):
        """CONNECTイベントを待ち受ける
        """

        print('start listen_connect_event')
        url = "/peers/{}/events?token={}".format(peer_id, peer_token)
        e = await loop.run_in_executor(None, async_get_event, url, "CONNECTION")
        data_connection_id = e["data_params"]["data_connection_id"]

        print('end listen_connect_event')
        return data_connection_id

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
    def close_data(cls, data_connection_id):
        """Dataの待受ポートの閉鎖要求を送信

        ----------
        :param data_connection_id: Dataを特定するためのID
        :return: None(正常終了)
        """
        res = request("delete", "/data/connections/{}".format(data_connection_id))
        if res.status_code == 204:
            print('release data connection')
            return None
        else:
            print('Failed closing data connection: ', res)
            exit()
