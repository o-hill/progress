import Vue from 'vue'
import Vuex from 'vuex'
import api from './api'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {

    networks: [ ]

  },
  mutations: {

    set_network_list(state, data) {
      state.networks = data.data['networks']
    }

  },
  actions: {

    list_networks(context) {
      api.get_networks().then((response) => {
        context.commit('set_network_list', response.data)
      })
    }

  }
})
