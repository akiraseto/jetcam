# todo:最後に外す(リモートデバッグ用コード)
import pydevd_pycharm

pydevd_pycharm.settrace('192.168.0.20', port=60000, stdoutToServer=True, stderrToServer=True)

import time
import subprocess
import queue
import threading
import json

from util import *
from peer import Peer
from media import Media
from data import Data
from robot import Robot

robot = Robot()


def listen_event(peer_id, peer_token, queue):
    """Peerオブジェクトのイベントを待ち受ける
    """

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
            Data.set_data_redirect(data_connection_id, data_id, "127.0.0.1", robot.port)

        elif res['event'] == 'OPEN':
            print('OPEN!')

        time.sleep(1)


def socket_loop(queue):
    # ソケット作成
    robot.make_socket()

    while True:
        data = robot.recv_data()
        data = data.decode(encoding="utf8", errors='ignore')
        queue.put({'data': data})
        robot.pin(data)


def listen_media_event(queue, media_connection_id):
    """MediaConnectionオブジェクトのイベントを待ち受ける
    """

    uri = "/media/connections/{}/events".format(media_connection_id)
    while True:
        _res = request('get', uri)
        res = json.loads(_res.text)

        if 'event' in res.keys():
            queue.put({'media_event': res['event']})

            if res['event'] in ['CLOSE', 'ERROR']:
                break

        else:
            print('No media_connection event')

        time.sleep(1)


if __name__ == '__main__':

    media_connection_id = ''
    data_connection_id = ''
    process_gst = None
    gst_cmd = "gst-launch-1.0 -e v4l2src ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! vp8enc deadline=1  ! rtpvp8pay pt=96 ! udpsink port={} host={} sync=false"
    SHUTDOWN_LIST = ['バルス', 'ばるす', 'balus', 'balusu', 'barusu', 'barus']

    peer_token = Peer.create_peer(API_KEY, PEER_ID)

    if peer_token is None:
        count_create = 1
        retry_PEER_ID = ''

        while peer_token is None:
            time.sleep(5)
            count_create += 1
            retry_PEER_ID = PEER_ID + str(count_create)
            peer_token = Peer.create_peer(API_KEY, retry_PEER_ID)

        PEER_ID = retry_PEER_ID

    peer_id, peer_token = Peer.listen_open_event(PEER_ID, peer_token)

    queue = queue.Queue()
    thread_listen_event = threading.Thread(target=listen_event, args=(peer_id, peer_token, queue))
    thread_listen_event.setDaemon(True)
    thread_listen_event.start()

    thread_socket = threading.Thread(target=socket_loop, args=(queue,))
    thread_socket.setDaemon(True)
    thread_socket.start()

    # todo:1 リファクタリングする
    # todo:2 LEGOと疎通する

    try:
        while True:
            results = queue.get()
            print(results)

            if 'data' in results.keys():
                if results['data'] in SHUTDOWN_LIST:
                    break

            elif 'media_connection_id' in results.keys():
                media_connection_id = results['media_connection_id']

                thread_media_event = threading.Thread(target=listen_media_event, args=(queue, media_connection_id))
                thread_media_event.setDaemon(True)
                thread_media_event.start()

            elif 'process_gst' in results.keys():
                process_gst = results['process_gst']

            elif 'data_connection_id' in results.keys():
                data_connection_id = results['data_connection_id']

            elif 'media_event' in results.keys():
                if results['media_event'] in ['CLOSE', 'ERROR']:
                    process_gst.kill()
                    Media.close_media_connections(media_connection_id)
                    Data.close_data_connections(data_connection_id)


    except KeyboardInterrupt:
        pass

    robot.close()
    Peer.close_peer(peer_id, peer_token)
    process_gst.kill()
    print('all shutdown!')
