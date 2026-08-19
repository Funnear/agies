"""Advanced Network Analytics & Predictive Intelligence for the Music Industry.

Includes:
1. Structural Holes & Burt's Constraint (Dealmakers spanning isolated clusters)
2. K-Core Network Shell Decomposition (Core vs Peripheral entities)
3. Collaboration & Pairing Link Predictor (Adamic-Adar, Jaccard, Resource Allocation)
4. Temporal Ecosystem Dynamics (Tracking network evolution across release eras)
"""

from collections import defaultdict
from typing import Any, Dict, List
import networkx as nx

from agies.graph.builder import MusicIndustryGraph
from agies.graph.schema import RelationshipType


class AdvancedIndustryAnalytics:
    """Advanced algorithmic analytics for music industry network dynamics."""

    def __init__(self, industry_graph: MusicIndustryGraph):
        self.mig = industry_graph
        self.mg = industry_graph.graph
        self._undirected: nx.Graph = industry_graph.to_simple_graph()

    def analyze_structural_holes(self, top_k: int = 8) -> List[Dict[str, Any]]:
        """Calculate Burt's Constraint to discover brokers spanning structural holes.

        Nodes with LOW network constraint have high structural hole autonomy
        (they bridge otherwise disconnected communities and control information/deal flows).
        """
        if len(self._undirected) < 3:
            return []

        # Burt's constraint is computed on connected components of size >= 3
        constraints = {}
        for comp in nx.connected_components(self._undirected):
            if len(comp) >= 3:
                sub = self._undirected.subgraph(comp)
                try:
                    c = nx.constraint(sub, weight="weight")
                    constraints.update(c)
                except Exception:
                    pass

        # Sort by constraint ascending (lowest constraint = highest autonomy / broker power)
        sorted_brokers = sorted(constraints.items(), key=lambda x: x[1])[:top_k]

        results = []
        for nid, score in sorted_brokers:
            ndata = self.mg.nodes.get(nid, {})
            results.append(
                {
                    "id": nid,
                    "name": ndata.get("name", nid),
                    "entity_type": ndata.get("entity_type"),
                    "network_constraint": round(score, 4),
                    "brokerage_potential": (
                        "Elite Bridge / Cross-Cluster Broker"
                        if score < 0.3
                        else "Moderate Broker"
                    ),
                    "degree": self._undirected.degree(nid),
                }
            )

        return results

    def compute_k_core_decomposition(self) -> Dict[str, Any]:
        """Perform K-core decomposition to identify innermost core vs peripheral players."""
        if len(self._undirected) == 0:
            return {"max_core": 0, "cores": {}}

        core_numbers = nx.core_number(self._undirected)
        max_k = max(core_numbers.values()) if core_numbers else 0

        grouped_by_core: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
        for nid, k in sorted(core_numbers.items(), key=lambda x: x[1], reverse=True):
            ndata = self.mg.nodes.get(nid, {})
            grouped_by_core[k].append(
                {
                    "id": nid,
                    "name": ndata.get("name", nid),
                    "entity_type": ndata.get("entity_type"),
                }
            )

        return {
            "max_core_level": max_k,
            "core_breakdown": {
                f"Core_Level_{k}": {
                    "count": len(members),
                    "prominent_members": [m["name"] for m in members[:6]],
                }
                for k, members in sorted(grouped_by_core.items(), reverse=True)
            },
        }

    def predict_future_collaborations(self, top_k: int = 10) -> List[Dict[str, Any]]:
        """Predict likely future musical collaborations using link prediction algorithms (Adamic-Adar & Jaccard)."""
        artists = set(self.mig.get_artists())
        if len(artists) < 2:
            return []

        # Candidate artist pairs without an existing COLLABORATED_WITH edge
        existing_collabs = set()
        for u, v, data in self.mg.edges(data=True):
            if data.get("rel_type") == RelationshipType.COLLABORATED_WITH.value:
                existing_collabs.add((u, v))
                existing_collabs.add((v, u))

        candidates = []
        artist_list = list(artists)
        for i in range(len(artist_list)):
            for j in range(i + 1, len(artist_list)):
                a1, a2 = artist_list[i], artist_list[j]
                if (a1, a2) not in existing_collabs:
                    candidates.append((a1, a2))

        if not candidates:
            return []

        predictions = []
        # Calculate Adamic-Adar index
        try:
            aa_scores = {
                (u, v): p
                for u, v, p in nx.adamic_adar_index(self._undirected, ebunch=candidates)
            }
        except Exception:
            aa_scores = {}

        # Calculate Jaccard coefficient
        try:
            jc_scores = {
                (u, v): p
                for u, v, p in nx.jaccard_coefficient(
                    self._undirected, ebunch=candidates
                )
            }
        except Exception:
            jc_scores = {}

        for u, v in candidates:
            score_aa = aa_scores.get((u, v), 0.0)
            score_jc = jc_scores.get((u, v), 0.0)

            # Combined affinity score
            combined_score = round(score_aa * 1.5 + score_jc * 2.0, 4)
            if combined_score > 0:
                name_u = self.mg.nodes.get(u, {}).get("name", u)
                name_v = self.mg.nodes.get(v, {}).get("name", v)
                genres_u = set(self.mg.nodes.get(u, {}).get("genres", []))
                genres_v = set(self.mg.nodes.get(v, {}).get("genres", []))
                common_genres = list(genres_u.intersection(genres_v))

                predictions.append(
                    {
                        "artist_1": name_u,
                        "artist_2": name_v,
                        "affinity_score": combined_score,
                        "shared_genres": common_genres,
                        "likelihood": (
                            "Very High"
                            if combined_score > 1.2
                            else "High" if combined_score > 0.6 else "Moderate"
                        ),
                    }
                )

        predictions.sort(key=lambda x: x["affinity_score"], reverse=True)
        return predictions[:top_k]

    def analyze_era_evolution(self) -> Dict[str, Any]:
        """Analyze network evolution across historical eras (Pre-2010, 2010-2019, 2020-Present)."""
        eras = {
            "Early_Eras (<=2009)": {"edges_count": 0, "active_collaborations": 0},
            "Streaming_Rise (2010-2019)": {
                "edges_count": 0,
                "active_collaborations": 0,
            },
            "Modern_Ecosystem (2020+)": {"edges_count": 0, "active_collaborations": 0},
        }

        for _, _, data in self.mg.edges(data=True):
            year = data.get("start_year")
            if not year:
                continue

            rel = data.get("rel_type")
            if year <= 2009:
                era_key = "Early_Eras (<=2009)"
            elif 2010 <= year <= 2019:
                era_key = "Streaming_Rise (2010-2019)"
            else:
                era_key = "Modern_Ecosystem (2020+)"

            eras[era_key]["edges_count"] += 1
            if rel == RelationshipType.COLLABORATED_WITH.value:
                eras[era_key]["active_collaborations"] += 1

        return eras
