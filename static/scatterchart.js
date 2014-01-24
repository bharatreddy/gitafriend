// Written by Bharat Kunduri
// Based on the D3 Scatter Plot Example --> http://bl.ocks.org/weiglemc/6185069
var callback = function (dataUser) {
  
  var dataset = new Array ();
  for (var i = 0; i < dataUser.length; i++) {
    dataset[i] = [ dataUser[i]['nflwrs'], dataUser[i]['nrepos'], dataUser[i]['login'] ];
  }

  var data = dataUser.slice();
  var nRepoFn = function(d) { return d.nrepos; }
  var dataXFn = function(d) { return d.nflwrs; }

  var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 375 - margin.top - margin.bottom;
  // // Commenting out the fish eye part
  // fisheye 
  // var fisheye = d3.fisheye.circular()
  //   .radius(100)
  //   .distortion(2);

  /* 
   * value accessor - returns the value to encode for a given data object.
   * scale - maps value to a visual display encoding, such as a pixel position.
   * map function - maps from data value to display value
   * axis - sets up axis
   */ 
  // setup x 
  var xValue = function(d) { return d.nflwrs;}, // data -> value
      xScale = d3.scale.linear().range([0, width]), // value -> display
      xMap = function(d) { return xScale(xValue(d));}, // data -> display
      xAxis = d3.svg.axis().scale(xScale).orient("bottom");
  // setup y
  var yValue = function(d) { return d.nrepos;}, // data -> value
      yScale = d3.scale.linear().range([height, 0]), // value -> display
      yMap = function(d) { return yScale(yValue(d));}, // data -> display
      yAxis = d3.svg.axis().scale(yScale).orient("left");
  // add the graph canvas to the body of the webpage
  var svg = d3.select("#d3Plot").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  // add the tooltip area to the webpage
  var tooltip = d3.select("#d3Plot").append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);
  // don't want dots overlapping axis, so add in buffer to data domain
  xScale.domain([d3.min(data, xValue)-1, d3.max(data, xValue)+1000]);
  yScale.domain([d3.min(data, yValue)-1, d3.max(data, yValue)+1]);
  // // Commenting out the fish eye part, wasnt working that well
  // // was slow for large number of datapoints.
  // svg.on("mousemove", function() {
  // fisheye.focus(d3.mouse(this));
  // svg.selectAll("circle")
  //     .each(function(d) {
  //       d.x = xMap(d);
  //       d.y = yMap(d);
  //       d.z = xMap(d)/500.;
  //       d.fisheye = fisheye(d);
  //     })
  //     .attr("cx", function(d) { return d.fisheye.x; })
  //     .attr("cy", function(d) { return d.fisheye.y; })
  //   .attr("r", function(d) { return d.fisheye.z * 2; })
  // });

  // x-axis
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("Num. Followers");
// y-axis
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Num. Repos");
// draw dots
  svg.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", function(d) { return xValue(d)/500. })
      .attr("cx", xMap)
      .attr("cy", yMap)
      .on("mouseover", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", .9);
          tooltip.html(d.login + "<br/> Followers : " + xValue(d) 
          + "<br/> Repositories : " + yValue(d) )
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(500)
               .style("opacity", 0);
      })
      .on("click", function(d) 
      { 
              window.open('https://github.com/'+d.login,'_blank'); 
      }); 

};
d3.json("/dataUser", callback);
dataset = callback;
// window.open('www.yourdomain.com','_blank');
// var data = [[5,3], [10,17], [15,4], [2,8]];
// console.log( data )