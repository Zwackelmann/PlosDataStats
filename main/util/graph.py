from string import Template
import json

t = Template("""
    <!DOCTYPE html>
    <meta charset="utf-8">
    <style>
        .link {
            fill: none;
            stroke: #666;
            stroke-width: 1.5px;
        }

        #licensing {
            fill: green;
        }

        .link.licensing {
            stroke: green;
        }

        .link.resolved {
            stroke-dasharray: 0,2 1;
        }

        circle {
            fill: #ccc;
            stroke: #333;
            stroke-width: 1.5px;
        }

        text {
            font: 10px sans-serif;
            pointer-events: none;
            text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, 0 -1px 0 #fff, -1px 0 0 #fff;
        }

    </style>
    <body>
    <script src="http://d3js.org/d3.v3.min.js"></script>
    <script>
    var links = $links;
    var nodeWeights = $nodeWeights
    var nodes = {};

    // Compute the distinct nodes from the links.
    links.forEach(function(link) {
        link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
        link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
    });

    var width = $width,
        height = $height;

    var animated = $animated;

    var force = d3.layout.force()
        .nodes(d3.values(nodes))
        .links(links)
        .size([width, height])
        .linkDistance(150)
        .on("tick", tick)

    if(!animated) {
        force
            .gravity(0)
            .charge(0)
            .linkStrength(0)
            .theta(0)
    } else {
        force
            .charge(-300)
            .gravity(0.05)
            .linkStrength(0.5)
    }
    
    force.start();

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    // Per-type markers, as they don't inherit styles.
    svg.append("defs").selectAll("marker")
        .data(["suit", "licensing", "resolved"])
          .enter().append("marker")
          .attr("id", function(d) { return d; })
          .attr("viewBox", "0 -5 10 10")
          .attr("refX", 15)
          .attr("refY", -1.5)
          .attr("markerWidth", 3)
          .attr("markerHeight", 3)
          .attr("orient", "auto")
        .append("path")
          .attr( "d", "M0,-5L10,0L0,5");

    var path = svg.append("g").selectAll("path")
            .data(force.links())
        .enter().append("path")
            .attr("fill", function(d) { return "none" })
            .attr("stroke", function(d) { 
                if(d.weight < 0.4) return "#BBB"
                else if (d.weight < 0.5) return "#AAA"
                else if (d.weight < 0.6) return "#888"
                else if (d.weight < 0.7) return "#666"
                else if (d.weight < 0.8) return "#444"
                else if (d.weight < 0.9) return "#222"
                else return "#000"
            })
            .attr("stroke-width", function(d) { return (d.weight*4) + "px" })

    var circle = svg.append("g").selectAll("circle")
            .data(force.nodes())
        .enter().append("circle")
            .attr("r", function(d) { 
                area = (0.05 + nodeWeights[d.name] * 0.95) * 100
                return Math.sqrt(area/Math.PI)
            })
            .call(force.drag);

    var text = svg.append("g").selectAll("text")
            .data(force.nodes())
        .enter().append("text")
            .attr("x", 8)
            .attr("y", ".1em")
            .text(function(d) { return d.name; });

    // Use elliptical arc path segments to doubly-encode directionality.
    function tick() {
        path.attr("d", linkArc);
        circle.attr("transform", transform);
        text.attr("transform", transform);
    }

    function linkArc(d) {
        var dx = d.target.x - d.source.x,
            dy = d.target.y - d.source.y,
            dr = 0// Math.sqrt(dx * dx + dy * dy);
        return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
    }

    function transform(d) {
        return "translate(" + d.x + "," + d.y + ")";
    }

    function stopAnimation() {
        force
            .gravity(0)
            .charge(0)
            .linkStrength(0)
            .theta(0)
            .start()
    }

    </script>
    <a href="#" onClick="stopAnimation()">stop animation</a>
    </body>
    """)

def getHtml(links, nodeWeights, width = 1000, height = 800, animated = True):
    animatedStr = "true"
    if not animated:
        animatedStr = "false"

    return t.substitute({ "links" : json.dumps(links), "nodeWeights" : json.dumps(nodeWeights), "width" : str(width),
        "height" : str(height), "animated" : animatedStr })

def writeGraphToFile(links, noteWeights, width=1000, height=800, animated=True, filename="graph.html"):
    f = open(filename, "w")
    f.write(getHtml(links, noteWeights, width, height, animated))
    f.close()
