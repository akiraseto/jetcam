# todo:最後に外す(リモートデバッグ用コード)
import pydevd_pycharm

pydevd_pycharm.settrace('192.168.0.11', port=60000, stdoutToServer=True, stderrToServer=True)

import sys
import subprocess

from util import *
from peer import Peer
from media import Media
from data import Data


def on_open(peer_id, peer_token):
    """skywayを使うためにgatewayを開放処理する

    ----------
    :param peer_id: 設定したいpeer_id
    :param peer_token: peer確立の際のtoken
    """

    print('on_open')

    (video_id, video_ip, video_port) = Media.create_media()
    (data_id, data_ip, data_port) = Data.create_data()

    # todo:非同期で実装
    media_connection_id = Media.listen_call_event(peer_id, peer_token)
    mc_id = media_connection_id
    Media.answer(media_connection_id, video_id)

    cmd = "gst-launch-1.0 -e v4l2src ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! vp8enc deadline=1  ! rtpvp8pay pt=96 ! udpsink port={} host={} sync=false".format(
        video_port, video_ip)
    process_gst = subprocess.Popen(cmd.split())

    # todo:非同期で実装
    data_connection_id = Data.listen_connect_event(peer_id, peer_token)
    dc_id = data_connection_id
    Data.set_data_redirect(data_connection_id, data_id, "127.0.0.1", 10000)

    return mc_id, dc_id, process_gst


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("please input peer id")
        exit()

    peer_id = sys.argv[1]
    skyway_api_key = API_KEY

    peer_token = Peer.create_peer(skyway_api_key, peer_id)

    # todo:非同期処理で実装する
    peer_id, peer_token = Peer.listen_open_event(peer_id, peer_token)
    media_connection_id, data_connection_id, process_gst = on_open(peer_id, peer_token)

    exit_flag = True
    while exit_flag:
        input_text = input()
        if input_text == "exit":
            exit_flag = False

    Media.close_media_connection(media_connection_id)
    Data.close_data(data_connection_id)
    Peer.close_peer(peer_id, peer_token)
    process_gst.kill()
