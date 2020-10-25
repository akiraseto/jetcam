import requests
import json
import socket

class Peer():
    def create_peer(self, key, peer_id):
        params = {
            "key": key,
            "domain": "localhost",
            "turn": False,
            "peer_id": peer_id,
        }
        res = requests.request("POST", "/peers", data= json.dumps(params))

        if res:
            res_body = json.loads(res.body)
            return res_body["params"]["token"]
        else:
            print(res)
            exit()

    def listen_open_event(self, peer_id, peer_token):
        pass
        # 非同期
        # async_get_event("/peers/{}/events?token={}".format(peer_id, peer_token), "OPEN")

    def close_peer(self, peer_id, peer_token):
        res = requests.request("DELETE", "/peers/{}?token={}".format(peer_id, peer_token))
        if res:
            return None
        else:
            print(res)
            exit()

