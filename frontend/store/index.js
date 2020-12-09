export const state = () => ({
  user: {
    uid: '',
    email: '',
    login: false,
  },
  skywayKey: '',
})

export const getters = {
  user: state => {
    return state.user
  },
  skywayKey: state => {
    return state.skywayKey
  },
}

export const actions = {
  login ({ dispatch }, payload) {
    this.$fire.auth.signInWithEmailAndPassword(payload.email, payload.password)
      .then(() => {
        console.log('login success！')
        dispatch('checkLogin')
        dispatch('getSkywayKey')
        this.$router.push('/operate')
      }).catch((error) => {
      alert(error)
    })
  },

  checkLogin ({ commit }) {
    this.$fire.auth.onAuthStateChanged(function (user) {
      if (user) {
        commit('getUser', {
          uid: user.uid,
          email: user.email
        })
        commit('switchLogin')
      }
    })
  },

  getSkywayKey ({ commit }) {
    this.$fire.firestore.collection('apis').doc('skyway').get()
      .then(doc => {
        if (!doc.exists) {
          console.log('firebase no document: not get skyway key')
        } else {
          const key = doc.data()
          commit('getSkywayKey', key['key'])
        }
      }).catch(err => {
      console.log('firebase Error', err)
    })
  },

  logout ({ commit }) {
    this.$fire.auth.signOut()
      .then(async () => {
        commit('releaseData')
        await commit('switchLogout')
        console.log('log out!')

      })
      .catch(err => {
        console.error(err)
      })
  }
}

export const mutations = {
  getUser (state, payload) {
    state.user.uid = payload.uid
    state.user.email = payload.email
  },

  switchLogin (state) {
    state.user.login = true
  },

  releaseData (state) {
    state.user.uid = ''
    state.user.email = ''
    state.skywayKey = ''
  },

  switchLogout (state) {
    state.user.login = false
  },

  getSkywayKey (state, payload) {
    state.skywayKey = payload
  },
}
