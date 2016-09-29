var h = 900;
var w = 900;
var N = 150;
var mu = 1.8;

var randomColor = (function(){
    var golden_ratio_conjugate = 0.618033988749895;
    var h = Math.random();

    var hslToRgb = function (h, s, l){
        var r, g, b;

        if(s == 0){
            r = g = b = l; // achromatic
        }else{
            function hue2rgb(p, q, t){
                if(t < 0) t += 1;
                if(t > 1) t -= 1;
                if(t < 1/6) return p + (q - p) * 6 * t;
                if(t < 1/2) return q;
                if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
                return p;
            }

            var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
            var p = 2 * l - q;
            r = hue2rgb(p, q, h + 1/3);
            g = hue2rgb(p, q, h);
            b = hue2rgb(p, q, h - 1/3);
        }

        return '#'+Math.round(r * 255).toString(16)+Math.round(g * 255).toString(16)+Math.round(b * 255).toString(16);
    };

    return function(){
        h += golden_ratio_conjugate;
        h %= 1;
        return hslToRgb(h, 0.5, 0.60);
    };
})();

var colors = []
for(i=0; i< 100; i++) {
    colors.push(randomColor());
}
console.log(colors);
d3.select("body").append("h1")
.text("Polya's Urn visualization with N="+N+" and \u03BC="+mu)
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

d3.csv("data/polya_data_N"+N+"_mu"+10*mu+".csv", function(rows) {
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
        .duration(200)
        .attrTween("fill", function(d,i,a) {
            return d3.interpolate(a, colors[d.k]);
        });
    });
});

