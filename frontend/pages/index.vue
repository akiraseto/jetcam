<template>
  <div class="container">
    <div>
      <ProjectTitle/>
      <Login/>
      <div class="links" v-if="user.login">
        <nuxt-link to="/operate">
          <b-button>
            <div>スタート</div>
          </b-button>
        </nuxt-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    user: function () {
      return this.$store.getters['user']
    },
  },

}
</script>

<style>

</style>
