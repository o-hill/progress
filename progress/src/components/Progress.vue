<template>

  <v-layout>
    <v-flex xs4>
      <v-card class='blue-grey pa-2 ma-3'>
        <v-list two-line>
          <template v-for='(network, index) in networks'>
            <v-list-tile @click='selectNetwork(index)' class='' :key=index>
              <v-list-tile-content>
                <v-list-tile-title>{{ network.title }}</v-list-tile-title>
                <v-list-tile-sub-title>{{ network.nPlots }} plots available.</v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-divider dark v-if="index + 1 < networks.length" :key="`divider-${index}`"></v-divider>
          </template>
        </v-list>
      </v-card>
    </v-flex>
    <v-flex xs8 class='scrollable'>
      <v-content class='pa-0'>
        <template>
          <graphs v-for='(metric, index) in selectedNetwork.plotData'
            :key='metric.name'
            :name='metric.name'
            :values='metric.data'
            :title='metric.title'
          ></graphs>
        </template>
      </v-content>
    </v-flex>
  </v-layout>

</template>


<script>

  import Graphs from './Graphs.vue'

  export default {

  name: 'Progress',

  	components: {
      Graphs
  	},

  	props: [ ],

  	data() {
  	  return {
  	    textInput: [ ]
  	  }
  	},

  	watch: {

  	},

  	methods: {

  	  setNPlots(index) {
  	    this.$store.dispatch('setNPlots', { 'index': index, 'nPlot': Number(this.textInput[index]) })
  	  },

  	  selectNetwork(index) {
  	    this.$store.dispatch('selectNetwork', { 'name': this.$store.state.networks[index].name })
  	  }

  	},

  	computed: {

  	  networks: {
  	    get: function() {
  	      // Populate the text input array as an array of empty strings.
  	      this.textInput = this.$store.state.networks.map((elt) => '')
  	      return this.$store.state.networks.sort((one, two) => { return one.name < two.name })
  	    }
  	  },

  	  selectedNetwork() {
  	    window.resizingFuncs = [ ]
  	    return this.$store.state.network
  	  }

  	},

  	mounted() {
      document.documentElement.style.overflow = 'hidden'
  	  this.$store.dispatch('list_networks')
  	}

  }

</script>


<style>

  .scrollable {
    position: absolute;
    top: 0;
    bottom: 5%;
    left: 33%;
    right: 0;
    overflow: auto;
  }

</style>
