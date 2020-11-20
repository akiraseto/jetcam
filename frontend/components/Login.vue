<template>
  <div class="login">

    <b-form @submit.prevent="login" v-if="! user.login">
      <b-form-group
        id="input-group-1"
        label="Email:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          placeholder="Enter email"
          required
          type="email"
          v-model="email"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        description="6文字以上"
        id="input-group-2"
        label="Password:"
        label-for="input-2"
      >
        <b-form-input
          id="input-2"
          placeholder="Enter password"
          required
          type="password"
          v-model="password"
        ></b-form-input>
      </b-form-group>

      <b-button
        class="button"
        type="submit"
        variant="primary">ログイン
      </b-button>

    </b-form>

  </div>
</template>


<script>
export default {
  data () {
    return {
      email: '',
      password: '',
    }
  },

  methods: {
    login () {
      this.$store.dispatch('login', {
        email: this.email,
        password: this.password
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
