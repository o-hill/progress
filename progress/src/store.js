import Vue from 'vue'
import Vuex from 'vuex'
import api from './api'

import { print } from 'graphql'
import gql from 'graphql-tag'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {

    networks: [ ],
    selectedNetwork: { }

  },
  mutations: {

    set_network_list(state, data) {
      state.networks = data.data['networks']
    },

    updateNetwork(state, data) {
      state.networks = [
        ...state.networks.filter(elt => elt.name !== data.name),
        data
      ]
    },

    setSelectedNetwork(state, data) {
      state.selectedNetwork = data
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
    },

    selectNetwork(context, data) {

      let query = gql`
        query networks ($name: String!) {
          networks (names: [$name]) {
            name
            nPlots
            plotNames
            plotData {
              title
              name
              data
            }
          }
        }`

      api.get(query, data).then((response) => {
        console.log(response)
        context.commit('setSelectedNetwork', response.data.data.networks[0])
      })
    }

  }
})
