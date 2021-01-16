<template>
  <div class="container">
    <div>

      <div class="input">
        <b-button @click="establish" :class="{ 'btn-success': peer }">
          Establish
        </b-button>
      </div>

      <div v-for="id in peersList" class="target-button" v-show="peer">
        <b-button v-show="id !== peerId" @click="setPartner(id)"
                  :class="{ 'btn-danger': id === targetId }">
          {{ id }}
        </b-button>
      </div>

      <div class="input">
        <b-button-group>
          <b-button @click="callOn" v-bind:disabled=" !targetId"
                    :class="{ 'btn-success': mediaConnection }">
            Call
          </b-button>
          <b-button @click="callOff" v-bind:disabled=" !mediaConnection">
            Stop
          </b-button>
        </b-button-group>

      </div>

      <video v-show="mediaConnection" id="remote_video" muted autoplay
             playsinline/>

      <div>
        <h3>Operation</h3>

        <b-card no-body bg-variant="light">
          <b-tabs card>
            <b-tab title="Default" active>
              <b-container fluid="sm">
                <b-row class="my-1">
                  <b-col sm="10">
                    <b-form-input id="lego-pan" v-model="ope.pan" type="range"
                                  min="-100" max="100" step="1"></b-form-input>
                    <div class="mb-1">{{ ope.pan }}</div>
                  </b-col>
                  <b-col sm="2" class="text-sm-left text-center">
                    <b-button @click="optimizeValue('pan')">PAN</b-button>
                  </b-col>
                </b-row>

                <b-row class="my-1">
                  <b-col sm="10">
                    <b-form-input id="lego-pedestal" v-model="ope.pedestal"
                                  type="range"
                                  min="-100" max="100" step="1"></b-form-input>
                    <div class="mb-1">{{ ope.pedestal }}</div>
                  </b-col>

                  <b-col sm="2" class="text-sm-left text-center">
                    <b-button @click="optimizeValue('pedestal')">PEDE</b-button>
                  </b-col>
                </b-row>

                <b-row class="my-1">
                  <b-col sm="10">
                    <b-form-input id="lego-tilt" v-model="ope.tilt" type="range"
                                  min="-100" max="100" step="1"></b-form-input>
                    <div class="mb-1">{{ ope.tilt }}</div>
                  </b-col>

                  <b-col sm="2" class="text-sm-left text-center">
                    <b-button @click="optimizeValue('tilt')">TILT</b-button>
                  </b-col>
                </b-row>

                <b-row class="my-1">
                  <b-col sm="10">
                    <b-button block class="btn-danger" @click="armStop">ARM STOP
                    </b-button>
                  </b-col>
                </b-row>

                <b-row class="mt-3">
                  <b-col sm="2">
                    <label for="message">Message:</label>
                  </b-col>
                  <b-col sm="8" class="mb-1">
                    <b-form-input id="message" v-model="message"
                                  type="text"></b-form-input>
                  </b-col>

                  <b-col sm="2" class="text-sm-left text-center">
                    <b-button @click="sendMessage">
                      SEND
                    </b-button>
                  </b-col>
                </b-row>
              </b-container>
            </b-tab>

            <b-tab title="Manual">
              <b-container fluid>
                <b-row class="mt-3">
                  <b-col sm="2">
                    <label for="target">Connect:</label>
                  </b-col>
                  <b-col sm="8" class="mb-1">
                    <b-form-input id="target" v-model="targetId"
                                  type="text"
                                  placeholder="Default: jetcam"></b-form-input>
                  </b-col>

                  <b-col sm="2" class="text-sm-left text-center">
                    <b-button @click="callOn" v-bind:disabled=" !targetId"
                              :class="{ 'btn-success': mediaConnection }">
                      Call
                    </b-button>
                  </b-col>
                </b-row>
                <hr>

                <b-row>
                  <b-col sm="10">
                    <b-button-group class="w-100 mb-2">
                      <b-button @click="setModule('pan')"
                                :class="{ 'btn-success': lego.move === 'pan' }">
                        PAN
                      </b-button>
                      <b-button @click="setModule('pedestal')"
                                :class="{ 'btn-success': lego.move === 'pedestal' }">
                        PEDE
                      </b-button>
                      <b-button @click="setModule('tilt')"
                                :class="{ 'btn-success': lego.move === 'tilt' }">
                        TILT
                      </b-button>
                    </b-button-group>
                  </b-col>
                </b-row>

                <b-row>
                  <b-col sm="2">
                    <label for="power">Power:</label>
                  </b-col>

                  <b-col sm="3" class="mb-1">
                    <b-form-input id="power" v-model="lego.power" type="number"
                                  min="-100" max="100" step="1">
                    </b-form-input>
                  </b-col>

                  <b-col sm="2">
                    <label for="time">Time:</label>
                  </b-col>

                  <b-col sm="3" class="mb-1">
                    <b-form-input id="time" v-model="lego.time" type="number"
                                  min="0" max="20" step="0.1">
                    </b-form-input>
                  </b-col>

                  <b-col sm="2" class="text-sm-left text-center">
                    <b-button @click="sendLegoOrder">
                      LEGO
                    </b-button>
                  </b-col>
                  <b-col>
                    <p class="text-danger small">Pedestal,TiltのPowerは正負逆</p>
                  </b-col>
                </b-row>

                <b-row class="my-1">
                  <b-col sm="10">
                    <b-button block class="btn-danger" @click="armStop">ARM STOP
                    </b-button>
                  </b-col>
                </b-row>

                <b-row class="mt-3">
                  <b-col sm="2">
                    <label for="message2">Message:</label>
                  </b-col>
                  <b-col sm="8" class="mb-1">
                    <b-form-input id="message2" v-model="message"
                                  type="text"></b-form-input>
                  </b-col>

                  <b-col sm="2" class="text-sm-left text-center">
                    <b-button @click="sendMessage">
                      SEND
                    </b-button>
                  </b-col>
                </b-row>
              </b-container>
            </b-tab>
          </b-tabs>
        </b-card>
      </div>

    </div>
  </div>
</template>

<script>
import Peer from 'skyway-js'

//todo:レイアウトを調整(スマホ意識)

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
      if (this.mediaConnection) {
        console.log('すでに接続しています。')
        return
      }


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
      console.log('全て切断しました。')
    },

    setModule(module) {
      if (this.lego.move === module) {
        this.lego.move = ''
      } else {

        this.lego.move = module
      }
    },

    //todo:send系をひとつにまとめる
    sendMessage() {
      if (!this.dataConnection) {
        console.log('データコネクションが接続されていません')
        return
      }

      console.log(this.message)
      let data = {
        message: this.message
      }

      this.dataConnection.send(JSON.stringify(data))
      this.message = ''
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

      this.sendLegoOrder(module)
    },

    sendLegoOrder(module = null) {
      if (!this.dataConnection) {
        console.log('データコネクションが接続されていません')
        return
      }

      console.log(this.lego)
      let data = {
        lego: this.lego
      }

      this.dataConnection.send(JSON.stringify(data))

      //初期化
      this.lego.move = ""
      this.lego.power = 0
      this.lego.time = 0

      if (module) {
        this.ope[module] = 0
      }
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
