"""Interactive Pyvis Graph Visualization for Music Industry Networks."""

from pathlib import Path
from pyvis.network import Network

from agies.graph.builder import MusicIndustryGraph
from agies.graph.schema import EntityType, RelationshipType


# Entity Color Palette
ENTITY_COLORS = {
    EntityType.ARTIST.value: "#4A90E2",  # Vibrant Blue
    EntityType.RECORD_LABEL.value: "#2ECC71",  # Emerald Green
    EntityType.PRODUCTION_HOUSE.value: "#1ABC9C",  # Teal
    EntityType.AGENCY.value: "#9B59B6",  # Amethyst Purple
    EntityType.STUDIO.value: "#E67E22",  # Warm Orange
    EntityType.PRODUCER.value: "#F1C40F",  # Golden Yellow
    EntityType.RELEASE.value: "#E74C3C",  # Crimson Red
    EntityType.TRACK.value: "#95A5A6",  # Slate Gray
}

# Edge Color Palette
RELATIONSHIP_COLORS = {
    RelationshipType.SIGNED_TO.value: "#2ECC71",
    RelationshipType.REPRESENTED_BY.value: "#9B59B6",
    RelationshipType.RECORDED_AT.value: "#E67E22",
    RelationshipType.PRODUCED_BY.value: "#F1C40F",
    RelationshipType.COLLABORATED_WITH.value: "#E74C3C",
    RelationshipType.PARENT_COMPANY_OF.value: "#34495E",
}


def render_interactive_graph(
    industry_graph: MusicIndustryGraph,
    output_html_path: str | Path = "music_industry_network.html",
    height: str = "750px",
    width: str = "100%",
    notebook: bool = False,
    heading: str = "Music Industry Entity-Relationship Ecosystem",
) -> Path:
    """Generate an interactive HTML network graph with physics and rich tooltips.

    Args:
        industry_graph: MusicIndustryGraph instance.
        output_html_path: Output file path for HTML graph.
        height: Canvas height.
        width: Canvas width.
        notebook: Whether rendering in a Jupyter Notebook cell.
        heading: Title displayed above graph.

    Returns:
        Path to the saved HTML file.
    """
    net = Network(
        height=height, width=width, directed=True, notebook=notebook, heading=heading
    )
    net.force_atlas_2based()

    # Pre-calculate degree for node sizing
    simple_g = industry_graph.to_simple_graph()
    degrees = dict(simple_g.degree()) if len(simple_g) > 0 else {}

    # Add Nodes
    for node_id, data in industry_graph.graph.nodes(data=True):
        etype = data.get("entity_type", "unknown")
        name = data.get("name", node_id)
        country = data.get("country", "N/A")
        genres = ", ".join(data.get("genres", [])) or "N/A"
        deg = degrees.get(node_id, 1)

        color = ENTITY_COLORS.get(etype, "#95A5A6")
        size = 14 + min(deg * 3, 30)

        title = f"""
        <div style='font-family:sans-serif; font-size:13px; line-height:1.4;'>
            <b>{name}</b><br/>
            <i>Type:</i> {etype.upper().replace('_', ' ')}<br/>
            <i>Country:</i> {country}<br/>
            <i>Genres:</i> {genres}<br/>
            <i>Connections:</i> {deg}
        </div>
        """

        shape = "dot"
        if etype in (EntityType.RECORD_LABEL.value, EntityType.PRODUCTION_HOUSE.value):
            shape = "box"
        elif etype == EntityType.AGENCY.value:
            shape = "diamond"
        elif etype == EntityType.STUDIO.value:
            shape = "square"

        net.add_node(
            node_id,
            label=name,
            title=title,
            color=color,
            size=size,
            shape=shape,
        )

    # Add Edges
    for u, v, data in industry_graph.graph.edges(data=True):
        rel = data.get("rel_type", "")
        color = RELATIONSHIP_COLORS.get(rel, "#BDC3C7")
        weight = data.get("weight", 1.0)
        is_cur = data.get("is_current", True)

        title_edge = f"Relationship: {rel}<br/>Current: {is_cur}<br/>Weight: {weight}"
        if data.get("start_year"):
            title_edge += f"<br/>Year: {data['start_year']}"

        net.add_edge(
            u,
            v,
            title=title_edge,
            color=color,
            value=weight * 2,
            dashes=not is_cur,  # Dashed line for expired / historical relationships
        )

    # Physics & interaction configuration
    net.set_options(
        """
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "maxVelocity": 50,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": { "iterations": 150 }
      },
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true
      }
    }
    """
    )

    out_file = Path(output_html_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    net.save_graph(str(out_file))

    return out_file
