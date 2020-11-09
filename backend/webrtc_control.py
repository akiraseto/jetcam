# todo:最後に外す(リモートデバッグ用コード)
import pydevd_pycharm

pydevd_pycharm.settrace('192.168.0.8', port=60000, stdoutToServer=True, stderrToServer=True)

import sys
import subprocess

from util import *
from peer import Peer
from media import Media
from data import Data


async def media_build(peer_id, peer_token):
    (video_id, video_ip, video_port) = await Media.create_media()

    media_connection_id = await Media.listen_call_event(peer_id, peer_token)
    Media.answer(media_connection_id, video_id)

    cmd = "gst-launch-1.0 -e v4l2src ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! vp8enc deadline=1  ! rtpvp8pay pt=96 ! udpsink port={} host={} sync=false".format(
        video_port, video_ip)
    process_gst = subprocess.Popen(cmd.split())

    print('media build')

    # return media_connection_id, process_gst
    return {'media_connection_id': media_connection_id, 'process_gst': process_gst}


async def data_build(peer_id, peer_token):
    (data_id, data_ip, data_port) = await Data.create_data()

    data_connection_id = await Data.listen_connect_event(peer_id, peer_token)
    Data.set_data_redirect(data_connection_id, data_id, "127.0.0.1", 10000)

    print('data build:')
    return {'data_connection_id': data_connection_id}


def on_open(peer_id, peer_token):
    """skywayを使うためにgatewayを開放処理する

    ----------
    :param peer_id: 設定したいpeer_id
    :param peer_token: peer確立の際のtoken
    """

    print('on_open')

    # todo:非同期
    loop = asyncio.get_event_loop()

    done, pending = loop.run_until_complete(asyncio.wait([
        media_build(peer_id, peer_token),
        data_build(peer_id, peer_token)
    ]))

    # (video_id, video_ip, video_port) = Media.create_media()
    # (data_id, data_ip, data_port) = Data.create_data()

    # todo:非同期で実装
    # media_connection_id = Media.listen_call_event(peer_id, peer_token)
    # mc_id = media_connection_id
    # Media.answer(media_connection_id, video_id)
    #
    # cmd = "gst-launch-1.0 -e v4l2src ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! vp8enc deadline=1  ! rtpvp8pay pt=96 ! udpsink port={} host={} sync=false".format(
    #     video_port, video_ip)
    # process_gst = subprocess.Popen(cmd.split())

    # todo:非同期で実装
    # data_connection_id = Data.listen_connect_event(peer_id, peer_token)
    # dc_id = data_connection_id
    # Data.set_data_redirect(data_connection_id, data_id, "127.0.0.1", 10000)

    # return mc_id, dc_id, process_gst
    return done


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("please input peer id")
        exit()

    peer_id = sys.argv[1]
    skyway_api_key = API_KEY

    peer_token = Peer.create_peer(skyway_api_key, peer_id)
    peer_id, peer_token = Peer.listen_open_event(peer_id, peer_token)

    done = on_open(peer_id, peer_token)
    results = {}
    for result in done:
        results.update(result.result())

    exit_flag = True
    while exit_flag:
        # todo:ここに listen_close_eventを書く
        # todo:クローズされてたら再度on_open()する

        input_text = input()
        if input_text == "exit":
            exit_flag = False

    Media.close_media_connection(results['media_connection_id'])
    Data.close_data(results['data_connection_id'])
    Peer.close_peer(peer_id, peer_token)
    results['process_gst'].kill()
