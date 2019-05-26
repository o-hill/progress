import axios from 'axios'
window.axios = axios

import { print } from 'graphql'


const BASE_URL = 'http://localhost:5000/graphql'

export default {

  get(apiquery, data) {
    return axios.post(BASE_URL, {
      query: print(apiquery),
      variables: data
    })
  },

  get_networks() {
    return axios.post(BASE_URL, {
      query: `{
        networks {
          name
          nPlots
        }
      }`
    })
  },

  post_mutation(mut, data) {
    return axios.post(BASE_URL, {
      query: print(mut),
      variables: data
    })
  }

}

