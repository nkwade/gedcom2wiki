import networkx as nx  # type: ignore

# Takes a family tree and generates an interactive graph of the family tree.
import plotly.graph_objects as go  # type: ignore


def generate_family_graph(ft, output_file="family_tree.html"):
    # Create a NetworkX graph
    G = nx.DiGraph()

    # First, add nodes for all individuals
    for person_id, person in ft.persons.items():
        # Create a label for the person
        label = person.names[0] if person.names else person_id
        G.add_node(person_id, label=label)

    # Now add edges based on families
    for family_id, family in ft.families.items():
        parents = []
        if family.husb and family.husb in ft.persons:
            parents.append(family.husb)
        if family.wife and family.wife in ft.persons:
            parents.append(family.wife)

        for child_id in family.children:
            if child_id in ft.persons:
                for p_id in parents:
                    G.add_edge(p_id, child_id)

    # Generate positions for each node
    pos = nx.spring_layout(G)

    # Create edge traces
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    # Create node traces
    node_x = []
    node_y = []
    node_text = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(G.nodes[node]["label"])

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        hoverinfo="text",
        marker=dict(color="lightblue", size=10, line_width=2),
    )

    # Create the figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Family Tree",
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    # Save the figure as an HTML file
    fig.write_html(output_file)
