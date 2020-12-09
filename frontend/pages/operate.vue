<template>
  <div class="container">
    <div>

      <div class="input">
        <b-button @click="establish" :class="{ 'btn-success': peer }">
          Establish
        </b-button>
      </div>

      <div v-for="id in peersList" class="target-button">
        <b-button v-show="id !== peerId" @click="setPartner(id)" :class="{ 'btn-danger': id === targetId }">
          {{ id }}
        </b-button>
      </div>

      <div class="input">
        <b-button @click="callOn" v-bind:disabled=" !targetId">
          Call
        </b-button>
        <b-button @click="callOff" v-bind:disabled=" !mediaConnection">
          Stop
        </b-button>
      </div>

      <div class="input">
        <label for="chat_box">Message</label>
        <input id="chat_box" v-model="message" type="text">
        <b-button @click="sendMessage" v-bind:disabled=" !dataConnection">
          send message
        </b-button>
      </div>

      <video id="remote_video" muted autoplay playsinline/>
    </div>
  </div>
</template>

<script>
import Peer from 'skyway-js'

export default {
  middleware: 'authenticated',
  data () {
    return {
      peer: null,
      peerId: process.env.peerId,
      peersList: [],
      targetId: '',
      message: '',
      mediaConnection: null,
      dataConnection: null,
      remoteStream: null
    }
  },

  computed: {
    skywayKey: function () {
      return this.$store.getters['skywayKey']
    },
    user: function () {
      return this.$store.getters['user']
    },
  },

  methods: {
    setPartner (partner_id) {
      this.targetId = partner_id

    },
    establish () {
      this.peer = new Peer(this.peerId, {
        key: this.skywayKey,
        debug: 3
      })

      this.peer.on('open', (id) => {
        console.log(id)

        this.peer.listAllPeers((peers) => {
          console.log(peers)
          this.peersList = peers
        })
      })

      this.peer.on('error', function (err) {
        alert(err.message)
      })
    },

    callOn () {
      this.remoteStream = document.getElementById('remote_video')

      //media streamの接続
      this.mediaConnection = this.peer.call(this.targetId, null, {
        videoReceiveEnabled: true
      })

      this.mediaConnection.on('stream', (stream) => {
        this.remoteStream.srcObject = stream

        this.mediaConnection.on('close', () => {
          console.log('ビデオ通話を切断しました。')
          this.remoteStream.srcObject.getTracks().forEach(track => track.stop())
          this.remoteStream.srcObject = null
          this.mediaConnection = null
        })

      })

      this.dataConnection = this.peer.connect(this.targetId)

      this.dataConnection.on('open', (data) => {
        console.log(data)

        this.dataConnection.on('close', () => {
          console.log('データ通信を切断しました。')
          this.dataConnection = null
        })

      })
    },

    callOff () {
      this.peer.destroy()
      this.peer = null

      this.targetId = ''
    },

    sendMessage () {
      console.log(this.message)
      this.dataConnection.send(this.message)
    }
  }
}
</script>

<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.input {
  margin: 20px 10px;
}

.target-button {
  margin: 10px 5px;
  display: inline-block;
}

</style>
