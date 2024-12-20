import os
import json
from typing import Dict
from ..gedcom.tree import FamilyTree, Person


def build_hierarchy(family_tree: FamilyTree) -> Dict:
    root_persons = [p for p in family_tree.persons.values() if len(p.famc) == 0]
    if not root_persons:
        root_persons = list(family_tree.persons.values())

    def person_to_node(p: Person) -> Dict:
        children_nodes = []
        for fam_id in p.fams:
            if fam_id in family_tree.families:
                fam = family_tree.families[fam_id]
                for c_id in fam.children:
                    if c_id in family_tree.persons:
                        c = family_tree.persons[c_id]
                        children_nodes.append(person_to_node(c))
        children_nodes.sort(key=lambda x: x.get("name", ""))
        display_name = p.name if p.name else p.xref_id
        return {
            "name": f"{display_name} ({p.xref_id})",
            "xref_id": p.xref_id,
            "children": children_nodes,
        }

    if len(root_persons) > 1:
        root_data = {
            "name": "Family Roots",
            "xref_id": "ROOTS",
            "children": [person_to_node(r) for r in root_persons],
        }
    else:
        root_data = person_to_node(root_persons[0])

    return root_data


def generate_hierarchical_tree(
    family_tree: FamilyTree, output_path: str, filename: str = "family_tree_static.html"
):
    os.makedirs(output_path, exist_ok=True)
    html_path = os.path.join(output_path, filename)

    data = build_hierarchy(family_tree)
    data_json = json.dumps(data)

    # Note: No 'f' prefix in the triple-quoted string now.
    # Use {{ and }} for literal braces in JS code.
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Family Tree</title>
<style>
body {{
    font-family: sans-serif;
    margin: 0;
    padding: 0;
    overflow: auto;
}}
.node rect {{
    fill: #fff;
    stroke: steelblue;
    stroke-width: 1.5px;
}}
.node text {{
    font: 12px sans-serif;
    fill: red; /* red and bold from previous request */
    font-weight: bold;
    pointer-events: none;
}}
.link {{
    fill: none;
    stroke: #ccc;
    stroke-width: 1.5px;
}}
</style>
</head>
<body>
<h1 style="text-align:center;">Family Tree</h1>
<div id="tree-container" style="width:100%; height:auto; overflow:auto;"></div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
var data = {data_json};

var svg = d3.select("#tree-container").append("svg");
var g = svg.append("g");

// Create a tree layout with spacing
var treemap = d3.tree()
    .nodeSize([200, 100]) 
    .separation((a, b) => (a.parent == b.parent ? 1.5 : 2));

var root = d3.hierarchy(data, d => d.children);
root = treemap(root);

// Create links
g.selectAll(".link")
    .data(root.links())
    .enter().append("path")
    .attr("class", "link")
    .attr("d", d => {{
        return "M" + d.source.x + "," + d.source.y
             + "C" + d.source.x + "," + (d.source.y + d.target.y)/2
             + " " + d.target.x + "," + (d.source.y + d.target.y)/2
             + " " + d.target.x + "," + d.target.y;
    }});

// Create nodes
var node = g.selectAll(".node")
    .data(root.descendants())
    .enter().append("g")
    .attr("class", "node")
    .attr("transform", d => "translate(" + d.x + "," + d.y + ")");

// Calculate rect width based on text length
node.each(function(d) {{
    d.textLength = d.data.name.length * 7;
}});

node.append("rect")
    .attr("width", d => d.textLength)
    .attr("height", 20)
    .attr("x", d => -d.textLength/2)
    .attr("y", -10)
    .attr("rx", 5)
    .attr("ry", 5);

node.append("text")
    .attr("dy", ".35em")
    .attr("text-anchor", "middle")
    .text(d => d.data.name);

// Add click event
node.on("click", (event, d) => {{
    if (d.data.xref_id && d.data.xref_id !== "ROOTS") {{
        var url = "persons/" + d.data.xref_id + ".html";
        window.open(url, "_blank");
    }}
}});

// Adjust SVG to fit all nodes
var minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
root.descendants().forEach(d => {{
  if (d.x < minX) minX = d.x;
  if (d.x > maxX) maxX = d.x;
  if (d.y < minY) minY = d.y;
  if (d.y > maxY) maxY = d.y;
}});

var padding = 50;
var fullWidth = (maxX - minX) + padding * 2;
var fullHeight = (maxY - minY) + padding * 2;

svg
    .attr("width", fullWidth)
    .attr("height", fullHeight);

g.attr("transform", "translate(" + (padding - minX) + "," + (padding - minY) + ")");
</script>
</body>
</html>
"""

    # Use format instead of f-string for data insertion
    html_content = html_template.format(data_json=data_json)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated: {html_path}")
