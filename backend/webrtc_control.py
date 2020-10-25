import sys
import os

from backend.peer import Peer
from backend.config import *


HOST = "localhost"
PORT = 8000

def on_open(peer_id, peer_token):
    print('on_open')

    # (video_id, video_ip, video_port) = create_media(true)
    # (data_id, data_ip, data_port) = create_data()


    p_id = ""
    mc_id = ""

    # th_call = listen_call_event(peer_id, peer_token)
    # 非同期処理

    # answer(video_id)
    cmd = "gst-launch-1.0 -e v4l2src ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! vp8enc deadline=1  ! rtpvp8pay pt=96 ! udpsink port=#{video_port} host=#{video_ip} sync=false"

    p_id = "cmd"

    dc_id = ""

    # th_connect = listen_connect_event(peer_id, peer_token)
    # set_data_redirect("127.0.0.1", 10000)




if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("please input peer id")
        exit()

    peer_id = sys.argv[1]

    skyway_api_key = API_KEY

    peer_token = Peer.create_peer(skyway_api_key, peer_id)

    media_connection_id = ""
    data_connection_id = ""
    process_id = ""

    # th_onopen = listen_open_event(peer_id, peer_token)
    # 非同期処理
    # (media_connection_id, data_connection_id, process_id) = on_open(peer_id, peer_token)



    exit_flag = True
    while exit_flag:
        input = sys.stdin.readline()
        if input == "exit":
            exit_flag = False

    # close_media_connection(media_connection_id)
    # close_peer(peer_id, peer_token)
    # Process.kill(: TERM, process_id)














