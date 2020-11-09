from util import *


class Peer:
    """SkyWayと接続しセッション管理を行う

    """

    @classmethod
    def create_peer(cls, key, peer_id):
        """Peerオブジェクトを生成し、SkyWayサーバと接続

        SkyWayサーバとアクセスするための情報を指定。正常接続で201を返す。

        ----------
        :param key: skywayのAPI KEY
        :param peer_id: 設定したいpeer_id
        """

        params = {
            "key": key,
            "domain": "localhost",
            "turn": False,
            "peer_id": peer_id,
        }
        res = request("post", "/peers", json.dumps(params))

        if res:
            res_text = json.loads(res.text)
            return res_text["params"]["token"]
        else:
            print('Failed creating peer port: ', res)
            exit()

    @classmethod
    def listen_open_event(cls, peer_id, peer_token):
        """OPENイベントを待ち受ける

        シグナリングサーバへ正常に接続できたかを確認
        """

        # todo: 非同期で実装する
        e = async_get_event("/peers/{}/events?token={}".format(peer_id, peer_token), "OPEN")

        peer_id = e["params"]["peer_id"]
        peer_token = e["params"]["token"]

        return peer_id, peer_token

    @classmethod
    def close_peer(cls, peer_id, peer_token):
        """Peerオブジェクトの開放処理

        Peerオブジェクトを開放し、全てのWebRTCセッションとデータ受け渡しのUDPポートをクローズ

        ----------
        :return: None(正常終了)
        """

        res = request("delete", "/peers/{}?token={}".format(peer_id, peer_token))
        if res.status_code == 204:
            print('release peer object')
            return None
        else:
            print('Failed releasing peer: ', res)
            exit()
