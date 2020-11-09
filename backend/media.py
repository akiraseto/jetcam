from util import *


class Media:
    """MediaStreamを利用する

    MediaConnectionオブジェクトと転送するメディアの送受信方法について指定
    """

    @classmethod
    async def create_media(cls, is_video=True):
        """Mediaの待受ポート開放要求を送信

        ----------
        :param is_video: MediaがVideoか指定(falseはAudio)
        :return: media_id, ip_v4, port
        """

        print('start create_media')
        loop = asyncio.get_event_loop()

        params = {
            "is_video": is_video
        }

        # res = request("post", "/media", json.dumps(params))
        res = await loop.run_in_executor(None, request, "post", "/media", json.dumps(params))

        if res.status_code == 201:
            json_text = json.loads(res.text)
            media_id = json_text["media_id"]
            ip_v4 = json_text["ip_v4"]
            port = json_text["port"]

            print('end create_media')
            return media_id, ip_v4, port

        else:
            print('Failed creating media port: ', res)
            exit()

    @classmethod
    async def listen_call_event(cls, peer_id, peer_token):
        """CALLイベントを待ち受ける
        """

        print('start listen_call_event')
        loop = asyncio.get_event_loop()

        # todo:非同期で実装する
        # e = async_get_event("/peers/{}/events?token={}".format(peer_id, peer_token), "CALL")
        e = await loop.run_in_executor(None, async_get_event, "/peers/{}/events?token={}".format(peer_id, peer_token),
                                       "CALL")
        media_connection_id = e["call_params"]["media_connection_id"]

        print('end listen_call_event')
        return media_connection_id

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
            "redirect_params": {}  # 相手からビデオを受け取らない
        }
        res = request("post", "/media/connections/{}/answer".format(media_connection_id), json.dumps(params))
        if res.status_code == 202:
            return json.loads(res.text)

        else:
            print('Failed answer: ', res)
            exit()

    @classmethod
    def close_media_connection(cls, media_connection_id):
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
            print('Failed closing media connection: ', res)
            exit()