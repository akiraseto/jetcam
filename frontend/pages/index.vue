<template>
  <div class="container">
    <div>
      <h1 class="title">jetcam</h1>
      <div class="input">
        <label for="apiKey">API KEY</label>
        <input type="text" id="apiKey" v-model="apiKey">
        <b-button v-on:click="establish">peer確立</b-button>
      </div>

      <div class="input">
        <ul v-for="peer in peersList">
          <li v-show="peer !== peerId">{{ peer }}</li>
        </ul>
      </div>

      <div class="input">
        <label for="target_id_box">接続先PEER ID</label>
        <input type="text" id="target_id_box" v-model="targetId">
        <b-button v-on:click="call_button">call</b-button>
      </div>

      <div class="input">
        <label for="chat_box">メッセージ</label>
        <input type="text" id="chat_box" v-model="message">
        <b-button v-on:click="chat_button">send message</b-button>
      </div>

      <video id="remote_video" muted="true" autoplay playsinline="true"></video>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      peer: null,
      connection: null,
      peerId: 'front',
      apiKey: '',
      peersList: [],
      targetId: '',
      message: '',
    }
  },

  methods: {
    establish() {
      this.peer = new Peer(this.peerId, {
        key: this.apiKey,
        debug: 3
      });

      this.peer.on('open', (id) => {
        console.log(id);

        this.peer.listAllPeers((peers) => {
          console.log(peers);
          this.peersList = peers;
        });
      });

      this.peer.on('error', function (err) {
        alert(err.message);
      });
    },

    call_button() {
      const call = this.peer.call(this.targetId, null, {
        videoReceiveEnabled: true
      });

      call.on('stream', (stream) => {
        document.getElementById("remote_video").srcObject = stream;
      });

      this.connection = this.peer.connect(this.targetId, {
        serialization: "none"
      });
      this.connection.on('data', (data) => {
        console.log(data);
      });
    },

    chat_button() {
      console.log(this.message);
      this.connection.send(this.message);
    }
  },

  mounted() {

  },
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

.title {
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.input {
  margin: 5px;
}
</style>
