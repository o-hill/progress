import Vue from 'vue'
import Vuex from 'vuex'
import api from './api'

import { print } from 'graphql'
import gql from 'graphql-tag'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {

    networks: [ ]

  },
  mutations: {

    set_network_list(state, data) {
      state.networks = data.data['networks']
    },

    updateNetwork(state, data) {
      // state.networks = state.networks.map((elt, idx) => {
      //   if (idx !== index) { return elt; }
      //   return data
      // })
      //

      console.log(data.name)

      state.networks = [
        ...state.networks.filter(elt => elt.name !== data.name),
        data
      ]
    }

  },
  actions: {

    list_networks(context) {
      api.get_networks().then((response) => {
        context.commit('set_network_list', response.data)
      })
    },

    setNPlots(context, data) {

      // Set up the mutation.
      const setPlots = gql`
      mutation updateNetwork($index:Int!, $nPlot:Int!) {
        updateNetwork (index:$index, nPlot:$nPlot) {
          name
          nPlots
        }
      }`

      api.post_mutation(setPlots, data).then((response) => {
        context.commit('updateNetwork', response.data.data.updateNetwork)
      })
    }

  }
})
