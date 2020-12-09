<template>
  <div>
    <b-navbar type="dark" variant="info">
      <b-navbar-brand to="/operate">jetCam</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-text disabled v-if="user.login">
            <span class="bold">ログイン中: {{ user.email }}</span>
          </b-nav-text>

          <b-nav-item
            @click="$bvModal.show('bv-modal-logout')"
            v-bind:disabled="! user.login">
            ログアウト
          </b-nav-item>

        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <b-modal hide-footer id="bv-modal-logout">
      <div class="d-block text-center">
        <p>ログアウトします。よろしいですか</p>
      </div>
      <b-button @click="logOut" block class="mt-3" variant="info">OK</b-button>
    </b-modal>

  </div>
</template>


<script>
export default {
  data () {
    return {
      data1: null
    }
  },

  methods: {
    logOut () {
      this.$bvModal.hide('bv-modal-logout')

      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/')
        })
    },

  },

  computed: {
    user () {
      return this.$store.getters['user']
    },
  },

}
</script>


<style>

</style>
