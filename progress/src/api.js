import axios from 'axios'
window.axios = axios

import { print } from 'graphql'


const BASE_URL = 'http://localhost:5000/graphql'

export default {

  call(apiquery, data=null) {
    return axios.post(BASE_URL, {
      query: print(apiquery),
      variables: data
    })
  }

}

