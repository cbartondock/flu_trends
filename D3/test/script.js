
/*var test_dataset = [
    [0,0,5],
    [10,10,0],
    [-5,2,3]];
var test2 = [1,2,3,4,5];
var w = 960, h = 500;
svg=d3.select("#chart").append("svg").attr("width",w).attr("height",h);
var text = svg.append("text").text("hello world").attr("y",50);
par = d3.select("body").append("p").text("New paragraph! How exciting")
d3.select("body").selectAll("p").data(test_dataset).enter().append("p").text(function(q) {return "The fucking number is " + q*q;});
bars = d3.select("body").selectAll("div").data(test_dataset).enter().append("div").attr("class","bar")
bars = bars.style("height",function (d) {return d*15+"px";});
*/

var h = 500;
var w = 500;

var color = d3.scale.linear().domain([0,5]).range(["red","blue"]);


var svg = d3.select("body").append("svg")
    .attr("width", w)
    .attr("height",h)
    .style("display","block")
    .style("margin","auto");

sb = d3.select("body").append("button")
    .style("width","50px")
    .style("background","#1FDA9A")
    .style("outline",0)
    .style("display","block").style("margin","auto")
    .text("Start!");

d3.csv("test.csv", function(rows) {
    svgcircles = svg.selectAll("circle").data(rows).enter()
        .append("circle")
        .attr("cx", function(d) { return w/2 + d.x*20; })
        .attr("cy", function(d) { return h/2 +d.y*20; })
        .attr("r", function(d) {return 10;})
        .attr("fill","white");

    sb.on('click', function(q) {
        svgcircles.data(rows).transition()
            .delay(function(d) {return d.t*300;})
            .duration(3000)
            .attr("fill", function(d) {return color(d.t);});
    });
});
