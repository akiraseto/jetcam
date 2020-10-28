import json
import socket

from util import *


class Data():

    @classmethod
    def create_data(self):
        res = request("post", "/data", "{}")
        if res:
            json_body = json.loads(res.body)
            data_id = json_body["data_id"]
            ip_v4 = json_body["ip_v4"]
            port = json_body["port"]
            return data_id, ip_v4, port
        else:
            print(res)
            exit()

    def listen_content_event(self, peer_id, peer_token):
        async_get_event("/peers/{}/events?token={}".format(peer_id, peer_token), "CONNECTION")

    def set_data_redirect(self, data_connection_id, data_id, redirect_addr, redirect_port):
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

    def close_data(self, data_connection_id):
        res = request("delete", "/data/connections/{}".format(data_connection_id))
        if res:
            return None
        else:
            print(res)
            exit()







