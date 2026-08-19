"""Graphify: Persistent Knowledge Graph Memory & Associative Recall Engine.

Transforms unstructured events, conversations, audio sessions, and entity discoveries
into an interconnected, multi-hop semantic and episodic graph memory network.

Capabilities:
1. Graphification: Entity and relation extraction from text and structured events
2. Multi-Hop Associative Recall: Traverse 1-hop and 2-hop neighborhood graphs
3. Episodic Memory Chains: Temporal sequencing and causal dependency tracking
4. Persistence: Disk-backed JSON storage and hot-reloading
"""

from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple
import networkx as nx

logger = logging.getLogger("agies.memory.graphify")


class MemoryNode:
    """A node within the Graphify memory network."""

    def __init__(
        self,
        node_id: str,
        label: str,
        node_type: str = "concept",  # 'concept', 'entity', 'episode', 'preference', 'acoustic_signature'
        attributes: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        importance: float = 1.0,
    ):
        self.node_id = node_id
        self.label = label
        self.node_type = node_type
        self.attributes = attributes or {}
        self.timestamp = timestamp or datetime.now(timezone.utc)
        self.importance = importance

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.node_id,
            "label": self.label,
            "node_type": self.node_type,
            "attributes": self.attributes,
            "timestamp": (
                self.timestamp.isoformat()
                if isinstance(self.timestamp, datetime)
                else str(self.timestamp)
            ),
            "importance": self.importance,
        }


class MemoryEdge:
    """A directed semantic or episodic relationship between memory nodes."""

    def __init__(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,  # 'RELATES_TO', 'MENTIONS', 'PREFERS', 'LEADS_TO', 'CLASSIFIED_AS', 'CO_OCCURS_WITH'
        weight: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.source_id = source_id
        self.target_id = target_id
        self.rel_type = rel_type
        self.weight = weight
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "rel_type": self.rel_type,
            "weight": self.weight,
            "metadata": self.metadata,
        }


class GraphifyMemory:
    """Graph-based Memory & Associative Recall Engine."""

    def __init__(self, memory_file_path: Optional[Path] = None):
        self.memory_file = Path(
            memory_file_path or (Path("data") / "memory" / "graph_memory.json")
        )
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self.graph: nx.MultiDiGraph = nx.MultiDiGraph()
        self._load_memory()

    def graphify_text(
        self,
        text: str,
        session_id: Optional[str] = None,
        context_tags: Optional[List[str]] = None,
        importance: float = 1.0,
    ) -> Dict[str, Any]:
        """Convert a text narrative, log, or conversation turn into interconnected memory nodes."""
        episode_id = f"ep_{int(datetime.now(timezone.utc).timestamp() * 1000)}"
        episode_node = MemoryNode(
            node_id=episode_id,
            label=text[:60] + ("..." if len(text) > 60 else ""),
            node_type="episode",
            attributes={
                "full_text": text,
                "session_id": session_id or "default_session",
                "tags": context_tags or [],
            },
            importance=importance,
        )
        self.add_node(episode_node)

        # Extract entities and key concepts
        extracted_concepts = self._extract_entities_and_concepts(text)
        created_nodes = [episode_id]

        for concept, ctype in extracted_concepts:
            concept_id = f"concept_{self._slugify(concept)}"
            if not self.graph.has_node(concept_id):
                c_node = MemoryNode(
                    node_id=concept_id,
                    label=concept,
                    node_type=ctype,
                    attributes={
                        "first_observed": datetime.now(timezone.utc).isoformat()
                    },
                )
                self.add_node(c_node)
                created_nodes.append(concept_id)

            # Link episode to concept
            self.add_edge(
                MemoryEdge(
                    source_id=episode_id,
                    target_id=concept_id,
                    rel_type="MENTIONS",
                    weight=1.0,
                )
            )

        # Cross-link concepts that co-occur in this episode
        concept_ids = [f"concept_{self._slugify(c)}" for c, _ in extracted_concepts]
        for i in range(len(concept_ids)):
            for j in range(i + 1, len(concept_ids)):
                c1, c2 = concept_ids[i], concept_ids[j]
                self.add_edge(
                    MemoryEdge(
                        source_id=c1,
                        target_id=c2,
                        rel_type="CO_OCCURS_WITH",
                        weight=0.8,
                        metadata={"episode_id": episode_id},
                    )
                )

        self._save_memory()
        return {
            "episode_id": episode_id,
            "created_nodes_count": len(created_nodes),
            "extracted_concepts": [c for c, _ in extracted_concepts],
            "total_memory_nodes": len(self.graph.nodes),
            "total_memory_edges": len(self.graph.edges),
        }

    def graphify_audio_event(
        self,
        track_title: str,
        artist_name: str,
        predicted_genre: str,
        confidence: float,
        detected_bpm: Optional[float] = None,
        provider: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Graphify an audio analysis event or search discovery into associative memory."""
        event_id = f"audio_event_{int(datetime.now(timezone.utc).timestamp() * 1000)}"
        event_node = MemoryNode(
            node_id=event_id,
            label=f"Audio Discovery: {track_title} ({predicted_genre})",
            node_type="episode",
            attributes={
                "track_title": track_title,
                "artist_name": artist_name,
                "predicted_genre": predicted_genre,
                "confidence": confidence,
                "detected_bpm": detected_bpm,
                "provider": provider,
            },
        )
        self.add_node(event_node)

        # Artist Node
        art_id = f"entity_{self._slugify(artist_name)}"
        if not self.graph.has_node(art_id):
            self.add_node(MemoryNode(art_id, artist_name, node_type="entity"))

        # Genre Node
        genre_id = f"genre_{self._slugify(predicted_genre)}"
        if not self.graph.has_node(genre_id):
            self.add_node(
                MemoryNode(genre_id, predicted_genre.title(), node_type="concept")
            )

        # Connect
        self.add_edge(MemoryEdge(event_id, art_id, "MENTIONS"))
        self.add_edge(MemoryEdge(art_id, genre_id, "CLASSIFIED_AS", weight=confidence))

        self._save_memory()
        return {"event_id": event_id, "artist_id": art_id, "genre_id": genre_id}

    def recall(
        self,
        query: str,
        hops: int = 2,
        top_k: int = 10,
    ) -> Dict[str, Any]:
        """Multi-hop associative recall starting from matched memory concepts."""
        matched_seeds: List[str] = []
        tokens = set(re.findall(r"\b\w+\b", query.lower()))

        for nid, data in self.graph.nodes(data=True):
            label = str(data.get("label", "")).lower()
            text = str(data.get("attributes", {}).get("full_text", "")).lower()
            if any(tok in label or tok in text for tok in tokens if len(tok) > 2):
                matched_seeds.append(nid)

        if not matched_seeds:
            return {
                "query": query,
                "recalled_nodes": [],
                "subgraph": {"nodes": [], "edges": []},
            }

        # Traverse multi-hop neighborhood
        recalled_node_ids: Set[str] = set(matched_seeds)
        current_frontier = set(matched_seeds)

        for _ in range(hops):
            next_frontier: Set[str] = set()
            for nid in current_frontier:
                # Successors and Predecessors in undirected view
                neighbors = set(self.graph.successors(nid)) | set(
                    self.graph.predecessors(nid)
                )
                for neighbor in neighbors:
                    if neighbor not in recalled_node_ids:
                        next_frontier.add(neighbor)
                        recalled_node_ids.add(neighbor)
            current_frontier = next_frontier

        # Score & Rank recalled items
        scored_nodes = []
        for nid in recalled_node_ids:
            data = self.graph.nodes[nid]
            degree = self.graph.degree(nid)
            importance = data.get("importance", 1.0)
            score = round(importance * (1.0 + 0.2 * degree), 3)
            scored_nodes.append(
                {
                    "id": nid,
                    "label": data.get("label", nid),
                    "node_type": data.get("node_type", "concept"),
                    "attributes": data.get("attributes", {}),
                    "relevance_score": score,
                }
            )

        scored_nodes.sort(key=lambda x: x["relevance_score"], reverse=True)
        top_nodes = scored_nodes[:top_k]
        top_ids = {n["id"] for n in top_nodes}

        # Build recalled subgraph
        sub_edges = []
        for u, v, k, d in self.graph.edges(keys=True, data=True):
            if u in top_ids and v in top_ids:
                sub_edges.append(
                    {
                        "source": u,
                        "target": v,
                        "rel_type": d.get("rel_type", "RELATES_TO"),
                        "weight": d.get("weight", 1.0),
                    }
                )

        return {
            "query": query,
            "matched_seeds_count": len(matched_seeds),
            "recalled_nodes_count": len(top_nodes),
            "recalled_nodes": top_nodes,
            "subgraph": {"nodes": top_nodes, "edges": sub_edges},
        }

    def add_node(self, node: MemoryNode):
        self.graph.add_node(node.node_id, **node.to_dict())

    def add_edge(self, edge: MemoryEdge):
        self.graph.add_edge(edge.source_id, edge.target_id, **edge.to_dict())

    def get_summary(self) -> Dict[str, Any]:
        """Return high-level memory statistics and top associative hubs."""
        degrees = dict(self.graph.degree())
        top_hubs = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:6]

        types_count: Dict[str, int] = {}
        for _, data in self.graph.nodes(data=True):
            ntype = data.get("node_type", "concept")
            types_count[ntype] = types_count.get(ntype, 0) + 1

        return {
            "total_nodes": len(self.graph.nodes),
            "total_edges": len(self.graph.edges),
            "node_types": types_count,
            "top_associative_hubs": [
                {
                    "id": nid,
                    "label": self.graph.nodes[nid].get("label", nid),
                    "connections": deg,
                }
                for nid, deg in top_hubs
            ],
            "memory_file": str(self.memory_file),
        }

    def _extract_entities_and_concepts(self, text: str) -> List[Tuple[str, str]]:
        """Extract recognized music, genre, country, and tech concepts from text."""
        concepts: List[Tuple[str, str]] = []
        t_low = text.lower()

        # Known keywords & entities dictionary
        patterns = [
            (
                r"\b(techno|house|trance|ambient|dubstep|drum and bass|classical|hip-hop|disco|rock|jazz)\b",
                "concept",
            ),
            (
                r"\b(germany|berlin|london|uk|usa|japan|tokyo|france|paris|sweden|stockholm|jamaica|nigeria|lagos)\b",
                "entity",
            ),
            (
                r"\b(hansa|funkhaus|kling klang|abbey road|electric lady|motorbass|tuff gong)\b",
                "entity",
            ),
            (
                r"\b(kraftwerk|david bowie|brian eno|daft punk|hans zimmer|nils frahm|taylor swift|drake|kendrick)\b",
                "entity",
            ),
            (
                r"\b(mel-spectrogram|tempogram|classifier|neural network|fastapi|knowledge graph|cosine similarity)\b",
                "concept",
            ),
        ]

        for pat, ctype in patterns:
            matches = re.findall(pat, t_low)
            for m in set(matches):
                concepts.append((m.title(), ctype))

        # Fallback if no specific entity matched: extract capitalized tokens
        if not concepts:
            words = [w for w in re.findall(r"\b[A-Z][a-z]+\b", text) if len(w) > 3]
            for w in set(words[:4]):
                concepts.append((w, "concept"))

        return concepts

    def _slugify(self, text: str) -> str:
        return re.sub(r"[^\w]+", "_", text.lower()).strip("_")

    def _save_memory(self):
        nodes_data = [d for _, d in self.graph.nodes(data=True)]
        edges_data = [d for _, _, d in self.graph.edges(data=True)]
        data = {
            "version": "1.0.0",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "nodes": nodes_data,
            "edges": edges_data,
        }
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _load_memory(self):
        if not self.memory_file.exists():
            return
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for n in data.get("nodes", []):
                self.graph.add_node(n["id"], **n)
            for e in data.get("edges", []):
                self.graph.add_edge(e["source_id"], e["target_id"], **e)
        except Exception as e:
            logger.warning("Could not load memory file %s: %s", self.memory_file, e)
