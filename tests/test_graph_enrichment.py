"""Unit tests for Acoustic Knowledge Graph Enrichment (arXiv:2110.08862)."""

from agies.graph.builder import MusicIndustryGraph
from agies.graph.enrichment import AcousticGraphEnricher
from agies.graph.schema import (
    Artist,
    Studio,
    Producer,
    RelationshipEdge,
    RelationshipType,
)


def test_acoustic_graph_enricher():
    graph = MusicIndustryGraph()

    # Add Artists
    a1 = Artist(id="art_techno_1", name="Berlin Pulse", genres=["Techno", "Industrial"])
    a2 = Artist(id="art_techno_2", name="Ostgut Resident", genres=["Techno", "Minimal"])
    a3 = Artist(id="art_trance_1", name="Euphoric Beam", genres=["Trance", "Uplifting"])
    std = Studio(id="std_hansa_test", name="Hansa Berlin", city="Berlin")
    prd = Producer(id="prd_test_1", name="Modulation Master", role="Techno Producer")

    graph.add_entity(a1)
    graph.add_entity(a2)
    graph.add_entity(a3)
    graph.add_entity(std)
    graph.add_entity(prd)

    graph.add_relationship(
        RelationshipEdge(
            source_id="art_techno_1",
            target_id="std_hansa_test",
            rel_type=RelationshipType.RECORDED_AT,
        )
    )
    graph.add_relationship(
        RelationshipEdge(
            source_id="art_techno_2",
            target_id="std_hansa_test",
            rel_type=RelationshipType.RECORDED_AT,
        )
    )
    graph.add_relationship(
        RelationshipEdge(
            source_id="art_techno_1",
            target_id="prd_test_1",
            rel_type=RelationshipType.PRODUCED_BY,
        )
    )

    enricher = AcousticGraphEnricher()
    results = enricher.enrich_graph(graph, similarity_threshold=0.80)

    assert results["enriched_artists_count"] == 3
    assert results["added_genre_nodes_count"] >= 1
    assert results["classified_edges_count"] == 3
    assert results["acoustic_similarity_edges_count"] >= 1

    # Check that genre edges exist
    edges = list(graph.graph.edges(data=True))
    classified_edges = [
        d for u, v, d in edges if d.get("rel_type") == "CLASSIFIED_AS_GENRE"
    ]
    assert len(classified_edges) == 3

    # Check acoustic similarity
    sim_edges = [d for u, v, d in edges if d.get("rel_type") == "ACOUSTIC_SIMILARITY"]
    assert len(sim_edges) >= 1
    assert sim_edges[0]["weight"] >= 0.80

    # Check studio and producer specialization
    assert (
        graph.graph.nodes["std_hansa_test"].get("dominant_acoustic_specialization")
        is not None
    )
    assert graph.graph.nodes["prd_test_1"].get("sonic_signature") is not None
