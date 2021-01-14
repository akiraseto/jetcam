import time
import queue as que
import threading

from peer import Peer
from media import Media
from data import Data
from robot import Robot
import config

# jetBrainsリモートデバッグ用モジュール
import pydevd_pycharm

pydevd_pycharm.settrace('192.168.0.20', port=60000,
                        stdoutToServer=True, stderrToServer=True)


def main():
    queue = que.Queue()
    robot = Robot()

    peer_id = config.PEER_ID
    media_connection_id = ''
    data_connection_id = ''
    process_gst = None

    peer_token = Peer.create_peer(config.API_KEY, peer_id)

    if peer_token is None:
        count_create = 1
        retry_peer_id = ''

        while peer_token is None:
            time.sleep(5)
            count_create += 1
            retry_peer_id = peer_id + str(count_create)
            peer_token = Peer.create_peer(config.API_KEY, retry_peer_id)

        peer_id = retry_peer_id

    peer_id, peer_token = Peer.listen_open_event(peer_id, peer_token)

    th_listen = threading.Thread(target=Peer.listen_event,
                                 args=(peer_id, peer_token, queue, robot))
    th_listen.setDaemon(True)
    th_listen.start()

    th_socket = threading.Thread(target=robot.socket_loop, args=(queue,))
    th_socket.setDaemon(True)
    th_socket.start()

    try:
        while True:
            results = queue.get()
            print(results)

            if 'message' in results.keys():
                if results['message'] in config.SHUTDOWN_LIST:
                    break

            elif 'media_connection_id' in results.keys():
                media_connection_id = results['media_connection_id']

                th_media = threading.Thread(target=Media.listen_media_event,
                                            args=(queue, media_connection_id))
                th_media.setDaemon(True)
                th_media.start()

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


if __name__ == '__main__':
    main()
