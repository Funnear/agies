"""Enterprise Neo4j Graph Database & Cypher Exporter.

Exports Music Industry Knowledge Graph to:
1. Production-ready Neo4j Cypher import script (.cypher)
2. Gephi / Cytoscape GraphML (.graphml)
3. Graph RAG semantic JSON (.json)
"""

import logging
from pathlib import Path
from typing import List, Optional

from agies.graph.builder import MusicIndustryGraph

logger = logging.getLogger("agies.graph.neo4j_exporter")


class Neo4jGraphExporter:
    """Exports MusicIndustryGraph into Neo4j Cypher and enterprise graph formats."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir or (Path("data") / "corpus"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_cypher(
        self, industry_graph: MusicIndustryGraph, filename: str = "neo4j_import.cypher"
    ) -> Path:
        """Generate Cypher statements with constraints and nodes/edges creation."""
        graph = industry_graph.graph
        out_path = self.output_dir / filename

        cypher_lines: List[str] = [
            "// ===================================================",
            "// AGIES Music Industry Knowledge Graph Cypher Import",
            "// Generated automatically for Neo4j / Memgraph",
            "// ===================================================\n",
            "// 1. Constraints & Unique Indexes",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Artist) REQUIRE a.id IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (l:RecordLabel) REQUIRE l.id IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Studio) REQUIRE s.id IS UNIQUE;\n",
            "// 2. Node Creation",
        ]

        # Export Nodes
        for nid, data in graph.nodes(data=True):
            etype = (
                str(data.get("entity_type", "Entity")).replace(" ", "_").capitalize()
            )
            name = str(data.get("name", nid)).replace('"', '\\"')
            country = str(data.get("country", "")).replace('"', '\\"')
            subgenre = str(data.get("classified_subgenre", "")).replace('"', '\\"')
            description = str(data.get("description", "")).replace('"', '\\"')
            bpm = data.get("detected_bpm", 0.0)

            cypher_lines.append(
                f'MERGE (n:{etype}:Entity {{id: "{nid}"}}) '
                f'ON CREATE SET n.name = "{name}", n.country = "{country}", '
                f'n.description = "{description}", '
                f'n.classified_subgenre = "{subgenre}", n.detected_bpm = {bpm};'
            )

        cypher_lines.append("\n// 3. Relationship Creation")

        # Export Edges
        for u, v, d in graph.edges(data=True):
            rel = str(d.get("rel_type", "RELATED_TO")).upper()
            weight = d.get("weight", 1.0)
            corridor = str(d.get("corridor_name", "")).replace('"', '\\"')

            cypher_lines.append(
                f'MATCH (a:Entity {{id: "{u}"}}), (b:Entity {{id: "{v}"}}) '
                f'MERGE (a)-[r:{rel} {{weight: {weight}, corridor_name: "{corridor}"}}]->(b);'
            )

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(cypher_lines))

        logger.info(
            "Exported Neo4j Cypher import script to %s (%d lines)",
            out_path,
            len(cypher_lines),
        )
        return out_path
