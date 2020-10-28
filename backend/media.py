import requests
import json
import socket

from util import *


class Media():
    @classmethod
    def create_media(cls, is_video):
        params = {
            "is_video": is_video
        }

        res = request("post", "/media", json.dumps(params))

        if res:
            json_body = json.loads(res.body)
            media_id = json_body["media_id"]
            ip_v4 = json_body["ip_v4"]
            port = json_body["port"]

            return media_id, ip_v4, port

        else:
            print(res)
            exit()

    def listen_call_event(self, peer_id, peer_token):
        pass
        # async_get_event("/peers/{}/events?token={}".format(peer_id, peer_token), "CALL")

    def answer(self, media_connection_id, video_id):
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
            return json.loads(res.body)

        else:
            print(res)
            exit()

    def listen_stream_event(self, media_connection_id):
        pass
        # async_get_event("/media/connections/#{}/events".format(media_connection_id), "STREAM")

    def close_media_connection(self,media_connection_id):
        res = request("delete", "/media/connections/{}".format(media_connection_id))
        if res:
            return None
        else:
            print(res)
            exit()

