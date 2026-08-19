"""Music Industry Knowledge Graph Builder & Network Manager."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import networkx as nx

from agies.graph.schema import (
    BaseEntity,
    EntityType,
    RelationshipEdge,
    RelationshipType,
)


class MusicIndustryGraph:
    """NetworkX-backed Knowledge Graph for the Music Industry ecosystem."""

    def __init__(self):
        # We use MultiDiGraph to allow multiple edges between same nodes (e.g. past vs current contract, collab)
        self.graph: nx.MultiDiGraph = nx.MultiDiGraph()
        self.entities_registry: Dict[str, BaseEntity] = {}

    def add_entity(self, entity: BaseEntity) -> None:
        """Add an entity node to the graph."""
        self.entities_registry[entity.id] = entity
        self.graph.add_node(
            entity.id,
            name=entity.name,
            entity_type=(
                entity.entity_type.value
                if hasattr(entity.entity_type, "value")
                else str(entity.entity_type)
            ),
            country=entity.country,
            genres=entity.genres,
            description=entity.description or entity.attributes.get("description", ""),
            attributes=entity.attributes,
        )

    def add_relationship(self, edge: RelationshipEdge) -> None:
        """Add a directed relationship edge between two entities."""
        if edge.source_id not in self.graph:
            raise KeyError(f"Source entity '{edge.source_id}' not found in graph.")
        if edge.target_id not in self.graph:
            raise KeyError(f"Target entity '{edge.target_id}' not found in graph.")

        rel_type_val = (
            edge.rel_type.value
            if hasattr(edge.rel_type, "value")
            else str(edge.rel_type)
        )

        self.graph.add_edge(
            edge.source_id,
            edge.target_id,
            key=f"{rel_type_val}_{edge.start_year or 'na'}",
            rel_type=rel_type_val,
            start_year=edge.start_year,
            end_year=edge.end_year,
            weight=edge.weight,
            is_current=edge.is_current,
            metadata=edge.metadata,
        )

    def ingest(self, entities: List[BaseEntity], edges: List[RelationshipEdge]) -> None:
        """Batch ingest entities and relationships."""
        for e in entities:
            self.add_entity(e)
        for rel in edges:
            if rel.source_id in self.graph and rel.target_id in self.graph:
                self.add_relationship(rel)

    def get_entity(self, entity_id: str) -> Optional[BaseEntity]:
        """Retrieve an entity object by its ID."""
        return self.entities_registry.get(entity_id)

    def get_nodes_by_type(self, entity_type: EntityType | str) -> List[str]:
        """Return list of node IDs of a given entity type."""
        t_val = entity_type.value if hasattr(entity_type, "value") else str(entity_type)
        return [
            node
            for node, data in self.graph.nodes(data=True)
            if data.get("entity_type") == t_val
        ]

    def get_artists(self) -> List[str]:
        """Get all artist node IDs."""
        return self.get_nodes_by_type(EntityType.ARTIST)

    def get_labels(self) -> List[str]:
        """Get all record label node IDs."""
        return self.get_nodes_by_type(EntityType.RECORD_LABEL)

    def get_studios(self) -> List[str]:
        """Get all studio node IDs."""
        return self.get_nodes_by_type(EntityType.STUDIO)

    def get_agencies(self) -> List[str]:
        """Get all agency node IDs."""
        return self.get_nodes_by_type(EntityType.AGENCY)

    def get_producers(self) -> List[str]:
        """Get all producer node IDs."""
        return self.get_nodes_by_type(EntityType.PRODUCER)

    def get_artist_ecosystem(self, artist_id: str) -> Dict[str, Any]:
        """Get complete ecosystem profile for an artist."""
        if artist_id not in self.graph:
            raise KeyError(f"Artist '{artist_id}' not found.")

        labels = []
        agencies = []
        studios = []
        producers = []
        collaborators = []

        # Outgoing edges from artist
        for _, target, data in self.graph.out_edges(artist_id, data=True):
            rel = data.get("rel_type")
            target_data = self.graph.nodes.get(target, {})
            entry = {
                "id": target,
                "name": target_data.get("name"),
                "is_current": data.get("is_current", True),
                "start_year": data.get("start_year"),
                "end_year": data.get("end_year"),
                "weight": data.get("weight", 1.0),
            }

            if rel == RelationshipType.SIGNED_TO.value:
                labels.append(entry)
            elif rel == RelationshipType.REPRESENTED_BY.value:
                agencies.append(entry)
            elif rel == RelationshipType.RECORDED_AT.value:
                studios.append(entry)
            elif rel == RelationshipType.PRODUCED_BY.value:
                producers.append(entry)
            elif rel == RelationshipType.COLLABORATED_WITH.value:
                collaborators.append(entry)

        # Incoming collaborations
        for source, _, data in self.graph.in_edges(artist_id, data=True):
            if data.get("rel_type") == RelationshipType.COLLABORATED_WITH.value:
                src_data = self.graph.nodes.get(source, {})
                collaborators.append(
                    {
                        "id": source,
                        "name": src_data.get("name"),
                        "weight": data.get("weight", 1.0),
                    }
                )

        return {
            "artist": self.graph.nodes[artist_id],
            "labels": labels,
            "agencies": agencies,
            "studios": studios,
            "producers": producers,
            "collaborators": collaborators,
        }

    def to_simple_graph(self) -> nx.Graph:
        """Convert MultiDiGraph to an undirected weighted Graph for algorithmic graph clustering & community detection."""
        g = nx.Graph()
        for node, data in self.graph.nodes(data=True):
            g.add_node(node, **data)

        for u, v, data in self.graph.edges(data=True):
            w = data.get("weight", 1.0)
            if g.has_edge(u, v):
                g[u][v]["weight"] = g[u][v].get("weight", 1.0) + w
            else:
                g.add_edge(u, v, weight=w, rel_type=data.get("rel_type"))

        return g

    def export_json(self, file_path: str | Path) -> None:
        """Export graph to JSON node-link format."""
        data = nx.node_link_data(self.graph)
        out = Path(file_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def summary(self) -> Dict[str, Any]:
        """Return summary statistics of the industry graph."""
        type_counts: Dict[str, int] = {}
        for _, data in self.graph.nodes(data=True):
            t = data.get("entity_type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1

        rel_counts: Dict[str, int] = {}
        for _, _, data in self.graph.edges(data=True):
            r = data.get("rel_type", "unknown")
            rel_counts[r] = rel_counts.get(r, 0) + 1

        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "nodes_by_type": type_counts,
            "edges_by_relationship": rel_counts,
        }
