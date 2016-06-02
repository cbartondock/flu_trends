var h = 900;
var w = 900;
var N = 100;
var mu = 1.8;


var color = d3.scale.linear().domain([0,N]).range(["red","black"]);


d3.select("body").append("h1")
    .text("Outbreak visualization with N="+N+" and \u03BC="+mu)
    .style("display","block")
    .style("margin-left","auto").style("margin-right","auto")
    .style("font-family","Palatino, serif");

var svg = d3.select("body").append("svg")
    .attr("width", w)
    .attr("height",h)
    .style("display","block")
    .style("margin","auto");

var sb = d3.select("body").append("button")
    .style("width","120px")
    .style("background","#1FDA9A")
    .style("outline",0)
    .style("display","block").style("margin","auto")
    .text("Play/Replay");

d3.csv("data/inf_data_N"+N+"_mu"+10*mu+".csv", function(rows) {
    var svgcircles = svg.selectAll("circle").data(rows).enter()
        .append("circle")
        .attr("cx", function(d) { return w/2 + d.x*1; })
        .attr("cy", function(d) { return h/2 +d.y*1; })
        .attr("r", 1)
        .attr("fill","white");

    sb.on('click', function(q) {
        svgcircles.transition()
            .attr("fill","white");
        svgcircles.data(rows).transition()
            .delay(function(d) {return d.t*150;})
            .duration(150)
            .attrTween("fill", function(d,i,a) {
                return d3.interpolate(a, color(d.t))
            ;});
    });
});
