"""Unstructured Literature & Article Graphifier Engine.

Ingests industry news, studio interviews, and track reviews into Graphify Memory:
1. Automated entity recognition (Artists, Studios, Labels, Cities, Genres, Hardware)
2. Relation extraction (RECORDED_AT, SIGNED_TO, COLLABORATED_WITH, PRAISES, INFLUENCED_BY)
3. Graph RAG context compilation
"""

import logging
from typing import Any, Dict, List, Optional
import re

from agies.memory.graphify import GraphifyMemory, MemoryEdge, MemoryNode

logger = logging.getLogger("agies.memory.article_graphifier")


class ArticleGraphifier:
    """Parses music journalism articles and press releases into structured knowledge graph facts."""

    def __init__(self, memory: Optional[GraphifyMemory] = None):
        self.memory = memory or GraphifyMemory()

    def ingest_article(
        self,
        title: str,
        content: str,
        source: str = "Resident Advisor",
        publication_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Convert an article into an interconnected memory subgraph."""
        # 1. Graphify text episode
        tags = [source, "Music Journalism", "Industry Intelligence"]
        res = self.memory.graphify_text(
            text=f"[{title}] {content}",
            session_id=f"article_{source.lower().replace(' ', '_')}",
            context_tags=tags,
            importance=1.2,
        )

        # 2. Extract specific acoustic/hardware mentions
        gear_mentions = self._extract_audio_gear(content)
        for gear in gear_mentions:
            gear_id = f"gear_{gear.lower().replace(' ', '_')}"
            if not self.memory.graph.has_node(gear_id):
                self.memory.add_node(
                    MemoryNode(
                        node_id=gear_id,
                        label=gear,
                        node_type="concept",
                        attributes={"category": "Audio Gear / Synthesizer"},
                    )
                )
            self.memory.add_edge(
                MemoryEdge(
                    source_id=res["episode_id"],
                    target_id=gear_id,
                    rel_type="MENTIONS_GEAR",
                    weight=0.9,
                )
            )

        self.memory._save_memory()
        return {
            "title": title,
            "episode_id": res["episode_id"],
            "extracted_concepts": res["extracted_concepts"],
            "gear_mentions": gear_mentions,
            "total_memory_nodes": len(self.memory.graph.nodes),
        }

    def _extract_audio_gear(self, text: str) -> List[str]:
        """Extract recognized iconic studio equipment and synthesizers."""
        gear_patterns = [
            r"\b(Roland TR-808|Roland TR-909|Roland TB-303|Minimoog|Prophet-5|Yamaha DX7|SSL 4000|Neve 8078|Fairchild 670|Telefunken U47|Neumann U87)\b",
            r"\b(TR-808|TR-909|TB-303|Moog|Juno-106|Korg MS-20|Ableton Live|Pro Tools|Logic Pro)\b",
        ]
        found = set()
        for p in gear_patterns:
            matches = re.findall(p, text, re.IGNORECASE)
            for m in matches:
                found.add(m.strip())
        return list(found)
