import json
import time
import subprocess

from util import request
from media import Media
from data import Data


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
            print('Success creating peer port: ', res)

            res_text = json.loads(res.text)
            return res_text["params"]["token"]
        else:
            print('Failed creating peer port: ', res)
            return None

    @classmethod
    def listen_open_event(cls, peer_id, peer_token):
        """OPENイベントを待ち受ける

        シグナリングサーバへ正常に接続できたかを確認
        """

        uri = "/peers/{}/events?token={}".format(peer_id, peer_token)
        res_json = None

        while res_json is None or res_json["event"] != 'OPEN':
            res = request('get', uri)

            if res.status_code == 200:
                res_json = json.loads(res.text)

        peer_id = res_json["params"]["peer_id"]
        peer_token = res_json["params"]["token"]

        return peer_id, peer_token

    @classmethod
    def listen_event(cls, peer_id, peer_token, queue, robot):
        """Peerオブジェクトのイベントを待ち受ける
        """

        gst_cmd = "gst-launch-1.0 -e v4l2src ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! vp8enc deadline=1 ! rtpvp8pay pt=96 ! udpsink port={} host={} sync=false"

        uri = "/peers/{}/events?token={}".format(peer_id, peer_token)
        while True:
            _res = request('get', uri)
            res = json.loads(_res.text)

            if 'event' not in res.keys():
                # print('No peer event')
                pass

            elif res['event'] == 'CALL':
                print('CALL!')
                media_connection_id = res["call_params"]["media_connection_id"]
                queue.put({'media_connection_id': media_connection_id})

                (video_id, video_ip, video_port) = Media.create_media()

                cmd = gst_cmd.format(video_port, video_ip)
                process_gst = subprocess.Popen(cmd.split())
                queue.put({'process_gst': process_gst})

                Media.answer(media_connection_id, video_id)

            elif res['event'] == 'CONNECTION':
                print('CONNECT!')
                data_connection_id = res["data_params"]["data_connection_id"]
                queue.put({'data_connection_id': data_connection_id})

                (data_id, data_ip, data_port) = Data.create_data()
                Data.set_data_redirect(data_connection_id, data_id, "127.0.0.1",
                                       robot.port)

            elif res['event'] == 'OPEN':
                print('OPEN!')

            time.sleep(1)

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
