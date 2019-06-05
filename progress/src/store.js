import Vue from 'vue'
import Vuex from 'vuex'
import api from './api'

import { print } from 'graphql'
import gql from 'graphql-tag'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {

    networks: [ ],
    network: { }

  },
  mutations: {

    setResources(state, data) {
      for (let resource in data.data) {
        if (resource in state)
          state[resource] = data.data[resource]
        else
          throw new Error('Resource not defined in state!')
      }
    },

  },

  actions: {

    list_networks(context) {
      let query = gql`
        query networks {
          networks {
            name
            title
            nPlots
          }
        }`

      api.call(query).then((response) => {
        context.commit('setResources', response.data)
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

      api.call(setPlots, data).then((response) => {
        context.commit('setResources', response.data)
      })
    },

    selectNetwork(context, data) {

      let query = gql`
        query networks ($name: String!) {
          network (name: $name) {
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

      api.call(query, data).then((response) => {
        console.log(response)
        context.commit('setResources', response.data)
      })
    }

  }
})
