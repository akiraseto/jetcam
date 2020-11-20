# todo:最後に外す(リモートデバッグ用コード)
import pydevd_pycharm

pydevd_pycharm.settrace('192.168.0.20', port=60000, stdoutToServer=True, stderrToServer=True)

import sys
import subprocess

from util import *
from peer import Peer
from media import Media
from data import Data
from robot import Robot

robot = Robot()


async def media_build(peer_id, peer_token, video_id, loop):
    media_connection_id = await Media.listen_call_event(peer_id, peer_token, loop)

    Media.answer(media_connection_id, video_id)
    return {'media_connection_id': media_connection_id}


async def data_build(peer_id, peer_token, data_id, loop):
    data_connection_id = await Data.listen_connect_event(peer_id, peer_token, loop)

    Data.set_data_redirect(data_connection_id, data_id, "127.0.0.1", robot.port)
    return {'data_connection_id': data_connection_id}


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("please input peer id")
        exit()

    peer_id = sys.argv[1]
    skyway_api_key = API_KEY

    peer_token = Peer.create_peer(skyway_api_key, peer_id)
    peer_id, peer_token = Peer.listen_open_event(peer_id, peer_token)

    # mediaの準備
    (video_id, video_ip, video_port) = Media.create_media()

    cmd = "gst-launch-1.0 -e v4l2src ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! vp8enc deadline=1  ! rtpvp8pay pt=96 ! udpsink port={} host={} sync=false".format(
        video_port, video_ip)
    process_gst = subprocess.Popen(cmd.split())

    # dataの準備
    (data_id, data_ip, data_port) = Data.create_data()

    # EVENT LOOP
    loop = asyncio.get_event_loop()
    done, pending = loop.run_until_complete(asyncio.wait([
        media_build(peer_id, peer_token, video_id, loop),
        data_build(peer_id, peer_token, data_id, loop)
    ]))

    results = {}
    for result in done:
        results.update(result.result())

    loop.close()

    # todo:接続待受機能を書く:一時後回し
    """
    event listenをマルチスレッド化して、callなど特定のresponseが来たら
    Queueでスレッドで渡してconnectしょりを書く？
    
    """

    # todo:firebase化する

    # ソケット作成
    robot.make_socket()

    try:
        while True:
            # Lチカ処理
            data = robot.recv_data()
            data = data.decode(encoding="utf8", errors='ignore')
            robot.pin(data)

    except KeyboardInterrupt:
        pass

    robot.close()
    Media.close_media_connection(results['media_connection_id'])
    Data.close_data(results['data_connection_id'])
    Peer.close_peer(peer_id, peer_token)
    process_gst.kill()
    print('terminate!')
