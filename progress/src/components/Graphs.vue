<template>

  <v-layout justify-center>
    <v-container class='pa-0 ma-3' fluid>
      <v-card class='' ref='card'>
        <v-card-title class='blue-grey display-1 white--text'>{{ this.title }}</v-card-title>
        <v-divider></v-divider>
        <svg width='100%' :id='"graph_" + this.name' ref='parent' height='500'></svg>
        <v-divider></v-divider>
        <v-layout class='blue-grey'>
          <v-flex xs4 class='pl-4'>
            <v-card-title class='white--text'>Iteration: {{ this.currentIteration }}</v-card-title>
            <v-card-title class='white--text'>Loss: {{ this.currentLoss }}</v-card-title>
          </v-flex>
          <v-flex xs4>
            <v-card-title class='white--text'>Most Recent Iteration Loss: {{ this.values.slice(-1)[0] }}</v-card-title>
            <v-card-title class='white--text'>
              Mean Loss: {{ this.values.reduce((a, b) => a + b) / this.values.length }}
            </v-card-title>
          </v-flex>
          <v-flex xs4>
            <v-card-title class='white--text'>Maximum Loss: {{ Math.max(...this.values) }}</v-card-title>
            <v-card-title class='white--text'>Minimum Loss: {{ Math.min(...this.values) }}</v-card-title>
          </v-flex>
        </v-layout>
      </v-card>
    </v-container>
  </v-layout>

</template>


<script>

  // import Component from '../componentLocation'

  export default {

  name: 'Graphs',

  	components: { },

  	props: {
  	  title: String,
  	  name: String,
  	  values: Array
  	},

  	data() {
  	  return {
  	    currentIteration: 0,
  	    currentLoss: 0
  	  }
  	},

  	watch: {

  	},

  	methods: {

  	  resizeGraph(first=false) {

  	    function transition(path) {
          path.transition()
            .duration(2500)
            .attrTween("stroke-dasharray", tweenDash)
            .each("end", function() { d3.select(this).call(transition); });
        }

        function tweenDash() {
          var l = this.getTotalLength(),
              i = d3.interpolateString("0," + l, l + "," + l);
          return function(t) { return i(t); };
        }

  	    d3.select('#graph_' + this.name).selectAll('*').remove()
  	    let bounding = this.$refs.parent.getBoundingClientRect()
  	    let that = this;

  	    let margin = 50;
  	    let width = bounding.width  - 2 * margin
  	    let height = 500 - margin

  	    let rect = d3.select('#graph_' + this.name).append('rect')
  	      .attr('x', margin + 5)
  	      .attr('y', margin - 30)
  	      .attr('width', width - 30)
  	      .attr('height', height - 30)
  	      .attr('id', 'bg_rect_' + this.name)
  	      .style('fill', '#edf4f8')

        let svg = d3.select('#graph_' + this.name).append('g')
          .attr('id', 'svg_group_' + this.name)

        //let data = [4, 2, 6, 7, 4, 5, 6, 8, 10, 4, 7, 6, 8, 6, 4, 5, 3, 0, 14]
        let data = this.values

        let x = d3.scaleLinear()
          .domain([0, data.length - 1])
          .range([margin + 20, width]);

        let y = d3.scaleLinear()
          .domain(d3.extent(data))
          .range([height - margin, margin]);

        let yAxis = d3.axisLeft(y).ticks(5)

        let line = d3.line()
          .curve(d3.curveMonotoneX)
          .x((d, i) => x(i))
          .y((d) => y(d));

        // Only animate the line the first time.
        if (first) {
          svg.append('path')
            .datum(data)
            .attr('class', 'data')
            .attr('id', 'data_path_' + this.name)
            .attr('fill', 'none')
            .attr('stroke', '#607e8a')
            .attr('stroke-width', 3)
        }
        else {
          svg.append('path')
            .attr('class', 'data')
            .attr('id', 'data_path_' + this.name)
            .attr('d', line(data))
            .attr('fill', 'none')
            .attr('stroke', '#607e8a')
            .attr('stroke-width', 3)
        }

        // Add the X Axis
        svg.append("g")
          .attr("class", "x axis")
          .attr('id', 'x_axis_' + this.name)
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

        // Add the Y Axis
        svg.append("g")
          .attr("class", "y axis")
          .attr('id', 'y_axis_' + this.name)
          .attr('transform', 'translate(' + (margin) + ',0)')
          .call(yAxis);

        // Now add titles to the axes
        svg.append("text")
          .attr("text-anchor", "middle")
          // Text is drawn off the screen top left, move down and out and rotate.
          .attr("transform", "translate(" + (margin / 2) + "," + (height / 2) + ")rotate(-90)")
          .text("Loss");

        // x axis label.
        svg.append("text")
          .attr("text-anchor", "middle")
          .attr("transform", "translate(" + (width / 2) + "," + (height + margin/1.1) + ")")
          .text("Training Iteration");

        this.$refs.parent.addEventListener('mousemove', (evt) => {
          svg.selectAll('.newdot').remove()
          const xPos = evt.clientX - bounding.left
          const iteration = Math.round(x.invert(xPos))

          svg.selectAll('.dot').data(data.filter((d, i) => i == iteration))
            .enter().append('circle')
            .attr('class', 'newdot')
            .attr('cx', (d, i) => x(iteration))
            .attr('cy', (d) => y(d))
            .attr('r', 5)
            .style('fill', '#ff4500')

          that.currentIteration = iteration
          that.currentLoss = data[iteration]
        })

        if (first) {
          if (!window.hasOwnProperty('resizingFuncs')) {
            window.resizingFuncs = [ ]
          }

          window.resizingFuncs.push(that.resizeGraph)

          window.onresize = () => {
            for (let i = 0; i < window.resizingFuncs.length; ++i) {
              window.resizingFuncs[i](false)
            }
          }

          svg.select('path.data')
            .datum(data)
            .attr('d', line)
            .call(transition)
        }
      }

  	},

  	computed: {

  	},

  	mounted() {

      console.log('mounted')
      this.resizeGraph(true)
  	}

  }

</script>


<style>


</style>
