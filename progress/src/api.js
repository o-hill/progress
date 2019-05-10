import axios from 'axios'
window.axios = axios


const BASE_URL = 'http:localhost:5000/graphql'

export default {

  get_networks() {
    return axios.post('http://localhost:5000/graphql', {
      query: `{
        networks {
          name
          nPlots
        }
      }`
    })
  }

}

