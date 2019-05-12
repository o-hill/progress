<template>

  <v-layout>
    <v-flex xs4>
      <v-card class='blue-grey pa-2 ma-3'>
        <v-list two-line>
          <template v-for='(network, index) in networks'>
            <v-list-tile @click='' class='' :key=index>
              <v-list-tile-content>
                <v-list-tile-title>{{ network.name }}</v-list-tile-title>
                <v-list-tile-sub-title>{{ network.nPlots }} plots available.</v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-text-field
                  :id="'input_' + index"
                  label='Number of Plots'
                  v-model='textInput[index]'
                ></v-text-field>
                <v-btn @click='setNPlots(index)'>Set</v-btn>
              </v-list-tile-action>
            </v-list-tile>
            <v-divider dark v-if="index + 1 < networks.length" :key="`divider-${index}`"></v-divider>
          </template>
        </v-list>
      </v-card>
    </v-flex>
    <v-flex xs8>
      <v-content><graphs/></v-content>
    </v-flex>
  </v-layout>

</template>


<script>

  // import Component from '../componentLocation'
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
  	  }

  	},

  	computed: {

  	  networks: {
  	    get: function() {
  	      console.log('computed')
  	      // Populate the text input array as an array of empty strings.
  	      this.textInput = this.$store.state.networks.map((elt) => '')
  	      return this.$store.state.networks.sort((one, two) => { return one.name < two.name })
  	    }
  	  }

  	},

  	mounted() {

  	  this.$store.dispatch('list_networks')

  	}

  }

</script>


<style>

</style>
