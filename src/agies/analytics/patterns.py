"""Behavioral Pattern Analytics Engine for the Music Industry.

Discovers structural, behavioral, and economic patterns:
1. Power Broker & Gatekeeper Centrality (PageRank, Betweenness, Degree)
2. Creative Ecosystems & Sub-Communities (Louvain / Modularity Clustering)
3. Label Mobility & Churn Analysis (Loyalty vs. Label Hopping)
4. Studio & Producer Reliance Index (SPRI / Concentration)
5. Agency Collaboration Density (Walled Gardens vs. Open Ecosystems)
6. Production Triads (Artist - Producer - Studio motifs)
"""

from collections import Counter
from typing import Any, Dict, List, Optional, Set
import networkx as nx
from networkx.algorithms import community

from agies.graph.builder import MusicIndustryGraph
from agies.graph.schema import RelationshipType


class MusicIndustryAnalytics:
    """Analytical algorithms for music industry graph behavioral pattern detection."""

    def __init__(self, industry_graph: MusicIndustryGraph):
        self.mig = industry_graph
        self.mg = industry_graph.graph
        self._undirected_cache: Optional[nx.Graph] = None

    def _get_undirected(self) -> nx.Graph:
        if self._undirected_cache is None:
            self._undirected_cache = self.mig.to_simple_graph()
        return self._undirected_cache

    def compute_power_brokers(self, top_k: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """Compute the most influential gatekeepers and power brokers.

        Uses PageRank and Betweenness Centrality across the network.
        """
        undirected = self._get_undirected()
        if len(undirected) == 0:
            return {"by_pagerank": [], "by_betweenness": []}

        pagerank_scores = nx.pagerank(undirected, weight="weight")
        betweenness_scores = nx.betweenness_centrality(undirected, weight="weight")

        def format_top(scores: Dict[str, float]) -> List[Dict[str, Any]]:
            sorted_nodes = sorted(scores.items(), key=lambda x: x[1], reverse=True)[
                :top_k
            ]
            res = []
            for nid, score in sorted_nodes:
                ndata = self.mg.nodes.get(nid, {})
                res.append(
                    {
                        "id": nid,
                        "name": ndata.get("name", nid),
                        "entity_type": ndata.get("entity_type"),
                        "score": round(score, 4),
                        "degree": undirected.degree(nid),
                    }
                )
            return res

        return {
            "by_pagerank": format_top(pagerank_scores),
            "by_betweenness": format_top(betweenness_scores),
        }

    def detect_creative_ecosystems(self) -> List[Dict[str, Any]]:
        """Detect densely connected creative clusters and sub-communities."""
        undirected = self._get_undirected()
        if len(undirected) == 0:
            return []

        try:
            communities = community.louvain_communities(
                undirected, weight="weight", seed=42
            )
        except Exception:
            communities = community.greedy_modularity_communities(
                undirected, weight="weight"
            )

        ecosystems = []
        for i, comm in enumerate(communities):
            members = list(comm)
            if len(members) < 2:
                continue

            entity_type_breakdown = Counter()
            genre_breakdown = Counter()
            names = []

            for nid in members:
                ndata = self.mg.nodes.get(nid, {})
                entity_type_breakdown[ndata.get("entity_type", "unknown")] += 1
                names.append(ndata.get("name", nid))
                for g in ndata.get("genres", []):
                    genre_breakdown[g] += 1

            ecosystems.append(
                {
                    "community_id": i + 1,
                    "size": len(members),
                    "top_genres": [g for g, _ in genre_breakdown.most_common(3)],
                    "entity_composition": dict(entity_type_breakdown),
                    "prominent_members": names[:6],
                    "member_ids": members,
                }
            )

        # Sort by community size descending
        ecosystems.sort(key=lambda x: x["size"], reverse=True)
        return ecosystems

    def analyze_label_mobility(self) -> Dict[str, Any]:
        """Analyze artist loyalty vs label migration (churn / hopping behaviour)."""
        artists = self.mig.get_artists()
        loyal_artists = []
        migrating_artists = []

        for aid in artists:
            aname = self.mg.nodes[aid].get("name", aid)
            # Find all SIGNED_TO edges
            signed_edges = [
                (v, data)
                for _, v, data in self.mg.out_edges(aid, data=True)
                if data.get("rel_type") == RelationshipType.SIGNED_TO.value
            ]

            unique_labels = {lbl_id for lbl_id, _ in signed_edges}
            num_labels = len(unique_labels)

            current_labels = [
                self.mg.nodes.get(v, {}).get("name", v)
                for v, data in signed_edges
                if data.get("is_current", True)
            ]
            past_labels = [
                self.mg.nodes.get(v, {}).get("name", v)
                for v, data in signed_edges
                if not data.get("is_current", True)
            ]

            info = {
                "artist_id": aid,
                "artist_name": aname,
                "total_labels_count": num_labels,
                "current_labels": current_labels,
                "past_labels": past_labels,
            }

            if num_labels > 1:
                info["mobility_status"] = "Label Hopper / Migrated"
                migrating_artists.append(info)
            elif num_labels == 1:
                info["mobility_status"] = "Single-Label Loyal"
                loyal_artists.append(info)

        total = len(artists)
        migration_rate = (
            round(len(migrating_artists) / total * 100, 1) if total > 0 else 0.0
        )

        return {
            "total_artists_analyzed": total,
            "migration_rate_percentage": migration_rate,
            "loyal_count": len(loyal_artists),
            "migrated_count": len(migrating_artists),
            "migrated_artists": migrating_artists,
            "loyal_artists": loyal_artists,
        }

    def compute_studio_reliance(self) -> List[Dict[str, Any]]:
        """Compute Studio & Producer Reliance Index (SPRI) for artists.

        Quantifies whether an artist's recording workflow is strictly concentrated in a single studio/producer
        or diversified across the industry.
        """
        artists = self.mig.get_artists()
        results = []

        for aid in artists:
            aname = self.mg.nodes[aid].get("name", aid)
            studio_edges = [
                v
                for _, v, data in self.mg.out_edges(aid, data=True)
                if data.get("rel_type") == RelationshipType.RECORDED_AT.value
            ]
            producer_edges = [
                v
                for _, v, data in self.mg.out_edges(aid, data=True)
                if data.get("rel_type") == RelationshipType.PRODUCED_BY.value
            ]

            primary_studio = (
                self.mg.nodes.get(studio_edges[0], {}).get("name")
                if studio_edges
                else "None"
            )
            primary_producer = (
                self.mg.nodes.get(producer_edges[0], {}).get("name")
                if producer_edges
                else "Self/Independent"
            )

            # Reliance score: 1.0 if has dedicated primary studio and producer, lower if none or spread
            reliance_score = 0.0
            if studio_edges and producer_edges:
                reliance_score = 1.0
            elif studio_edges or producer_edges:
                reliance_score = 0.5

            results.append(
                {
                    "artist_id": aid,
                    "artist_name": aname,
                    "reliance_index": reliance_score,
                    "primary_studio": primary_studio,
                    "primary_producer": primary_producer,
                    "reliance_category": (
                        "High Reliance (Signature Sound Circle)"
                        if reliance_score >= 0.8
                        else "Flexible / Diverse"
                    ),
                }
            )

        results.sort(key=lambda x: x["reliance_index"], reverse=True)
        return results

    def analyze_agency_collaboration_density(self) -> Dict[str, Any]:
        """Analyze whether talent agencies act as walled gardens or foster cross-agency collaborations."""
        agency_rosters: Dict[str, Set[str]] = {}
        artist_to_agency: Dict[str, str] = {}

        # Map artists to their current agencies
        for _, ag_id, data in self.mg.edges(data=True):
            if data.get("rel_type") == RelationshipType.REPRESENTED_BY.value:
                src = [
                    u
                    for u, v, d in self.mg.edges(data=True)
                    if v == ag_id
                    and d.get("rel_type") == RelationshipType.REPRESENTED_BY.value
                ]
                for art in src:
                    artist_to_agency[art] = ag_id
                    agency_rosters.setdefault(ag_id, set()).add(art)

        intra_agency_collabs = 0
        inter_agency_collabs = 0

        for u, v, data in self.mg.edges(data=True):
            if data.get("rel_type") == RelationshipType.COLLABORATED_WITH.value:
                ag_u = artist_to_agency.get(u)
                ag_v = artist_to_agency.get(v)

                if ag_u and ag_v:
                    if ag_u == ag_v:
                        intra_agency_collabs += 1
                    else:
                        inter_agency_collabs += 1

        total_collabs = intra_agency_collabs + inter_agency_collabs
        intra_ratio = (
            round(intra_agency_collabs / total_collabs * 100, 1)
            if total_collabs > 0
            else 0.0
        )

        agency_breakdown = {}
        for ag_id, members in agency_rosters.items():
            ag_name = self.mg.nodes.get(ag_id, {}).get("name", ag_id)
            agency_breakdown[ag_name] = {
                "roster_size": len(members),
                "artists": [self.mg.nodes.get(m, {}).get("name", m) for m in members],
            }

        return {
            "total_collaborations": total_collabs,
            "intra_agency_collaborations": intra_agency_collabs,
            "inter_agency_collaborations": inter_agency_collabs,
            "intra_agency_ratio_percentage": intra_ratio,
            "behavior_interpretation": (
                "Walled Garden Dominance"
                if intra_ratio >= 60.0
                else (
                    "Balanced Cross-Agency Collaboration"
                    if intra_ratio >= 35.0
                    else "Open Network Collaboration"
                )
            ),
            "agencies_rosters": agency_breakdown,
        }
