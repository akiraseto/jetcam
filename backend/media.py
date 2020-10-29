import requests
import json
import socket

from util import *


class Media():
    """MediaStreamを利用する

    MediaConnectionオブジェクトと転送するメディアの送受信方法について指定
    """

    @classmethod
    def create_media(cls, is_video):
        """Mediaの待受ポート開放要求を送信

        ----------
        :param is_video: MediaがVideoか指定(falseはAudio)
        :return: media_id, ip_v4, port
        """
        params = {
            "is_video": is_video
        }

        res = request("post", "/media", json.dumps(params))

        if res:
            json_text = json.loads(res.text)
            media_id = json_text["media_id"]
            ip_v4 = json_text["ip_v4"]
            port = json_text["port"]

            return media_id, ip_v4, port

        else:
            print(res)
            exit()


    @classmethod
    def listen_call_event(cls, peer_id, peer_token):
        # todo:非同期で実装
        pass
        # async_get_event("/peers/{}/events?token={}".format(peer_id, peer_token), "CALL")


    @classmethod
    def answer(cls, media_connection_id, video_id):
        """callに応答する

        callにどのように応答するかMediaConstraintsを提供する。

        ----------
        :param media_connection_id:MediaConnection特定のid
        :param video_id:メディアid
        :return:レスポンスのオブジェクト
        """
        constraints = {
            "video": True,
            "videoReceiveEnabled": False,
            "audio": False,
            "audioReceiveEnabled": False,
            "video_params": {
                "band_width": 1500,
                "codec": "VP8",
                "media_id": video_id,
                "payload_type": 96,
            }
        }
        params = {
            "constraints": constraints,
            "redirect_params": {}  # 相手側からビデオを受け取らないため、redirectの必要がない
        }
        res = request("post", "/media/connections/{}/answer".format(media_connection_id), json.dumps(params))
        if res:
            return json.loads(res.text)

        else:
            print(res)
            exit()


    @classmethod
    def listen_stream_event(cls, media_connection_id):
        # todo:非同期で実装
        pass
        # async_get_event("/media/connections/#{}/events".format(media_connection_id), "STREAM")


    @classmethod
    def close_media_connection(cls,media_connection_id):
        """MediaConnectionを解放する

        ----------
        :param media_connection_id: MediaConnection特定のid
        :return: None(正常終了)
        """
        res = request("delete", "/media/connections/{}".format(media_connection_id))
        if res.status_code == 204:
            print('release media connection')
            return None
        else:
            print(res)
            exit()

