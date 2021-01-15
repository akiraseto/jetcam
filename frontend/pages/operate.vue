<template>
  <div class="container">
    <div>

      <div class="input">
        <b-button @click="establish" :class="{ 'btn-success': peer }">
          Establish
        </b-button>
      </div>

      <div v-for="id in peersList" class="target-button">
        <b-button v-show="id !== peerId" @click="setPartner(id)"
                  :class="{ 'btn-danger': id === targetId }">
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

      <video v-show="mediaConnection" id="remote_video" muted autoplay
             playsinline/>

      <b-container fluid>
        <h2>Operation</h2>

        <b-row class="my-1">
          <b-col sm="11">
            <b-form-input id="lego-pan" v-model="ope.pan" type="range"
                          min="-100" max="100" step="1"></b-form-input>
            <div class="mb-1">{{ ope.pan }}</div>
          </b-col>
          <b-col sm="1">
            <b-button @click="optimizeValue('pan')">PAN</b-button>
          </b-col>
        </b-row>

        <b-row class="my-1">
          <b-col sm="11">
            <b-form-input id="lego-pedestal" v-model="ope.pedestal" type="range"
                          min="-100" max="100" step="1"></b-form-input>
            <div class="mb-1">{{ ope.pedestal }}</div>
          </b-col>
          <b-col sm="1">
            <b-button @click="optimizeValue('pedestal')">PEDESTAL</b-button>
          </b-col>
        </b-row>

        <b-row class="my-1">
          <b-col sm="11">
            <b-form-input id="lego-tilt" v-model="ope.tilt" type="range"
                          min="-100" max="100" step="1"></b-form-input>
            <div class="mb-1">{{ ope.tilt }}</div>
          </b-col>
          <b-col sm="1">
            <b-button @click="optimizeValue('tilt')">TILT</b-button>
          </b-col>
        </b-row>

        <b-row class="my-1">

          <b-col sm="11">
            <b-button block class="btn-danger" @click="armStop">ARM STOP
            </b-button>
          </b-col>

        </b-row>

        <b-row class="mt-3 mb-1">
          <b-col sm="2">
            <label for="message">Message:</label>
          </b-col>
          <b-col sm="9">
            <b-form-input id="message" v-model="message"
                          type="text"></b-form-input>
          </b-col>
          <b-col sm="1">
            <b-button @click="sendMessage">
              SEND
            </b-button>
          </b-col>
        </b-row>

      </b-container>

    </div>
  </div>
</template>

<script>
import Peer from 'skyway-js'

export default {
  middleware: 'authenticated',
  data() {
    return {
      peer: null,
      peerId: process.env.peerId,
      peersList: [],
      targetId: '',
      message: '',
      mediaConnection: null,
      dataConnection: null,
      remoteStream: null,
      lego: {
        move: "",
        power: 0,
        time: 0
      },
      ope: {
        pan: 0,
        pedestal: 0,
        tilt: 0
      }
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
    setPartner(partner_id) {
      this.targetId = partner_id

    },
    establish() {
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

    callOn() {
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

    callOff() {
      this.peer.destroy()
      this.peer = null

      this.targetId = ''
    },

    sendMessage() {
      console.log(this.message)

      let data = {
        message: this.message
      }

      this.dataConnection.send(JSON.stringify(data))
    },

    optimizeValue(module) {
      this.lego.move = module
      let value = this.ope[module]
      let plusMinus = 1

      //+-を確認
      if (value === 0) {
        return
      } else if (value < 0) {
        plusMinus = -1
        value = Math.abs(value)
      }

      //挙動の調整
      if (value < 40) {
        this.lego.power = plusMinus
        this.lego.time = value / 10

      } else if (40 <= value && value < 70) {
        this.lego.power = 3 * plusMinus
        this.lego.time = value / 15

      } else if (70 <= value) {
        this.lego.power = 9 * plusMinus
        this.lego.time = value / 20

      }

      // pedestal、tilt 動きと値が正負逆なので調整
      if (['pedestal', 'tilt'].includes(module)) {
        this.lego.power = this.lego.power * -1
      }

      this.sendLegoOrder()

      //初期化
      this.lego.move = ""
      this.lego.power = 0
      this.lego.time = 0
      this.ope[module] = 0
    },

    sendLegoOrder() {
      console.log(this.lego)
      let data = {
        lego: this.lego
      }

      this.dataConnection.send(JSON.stringify(data))
    },

    armStop() {
      this.lego.move = 'stop'
      this.sendLegoOrder()

      this.lego.move = ''
    },
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
