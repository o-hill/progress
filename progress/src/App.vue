<template>
  <v-app>
    <v-toolbar app class='blue-grey'>
      <v-toolbar-title class="headline text-uppercase">
        <span>ML</span>
        <span class="font-weight-light">TRAINING PROGRESS</span>
      </v-toolbar-title>
    </v-toolbar>

    <v-content>
      <Progress/>
    </v-content>
    <v-footer class='blue-grey' fixed>
      <!-- <v-spacer></v-spacer> -->
      <div class='ml-4'>&copy; Michigan Aerospace Corporation {{ new Date().getFullYear() }}</div>
    </v-footer>
  </v-app>
</template>

<script>
import Progress from './components/Progress'
import Graphs from './components/Graphs'

export default {
  name: 'App',
  components: {
    Progress,
    Graphs
  },
  data () {
    return {
      //
    }
  }
}
</script>
