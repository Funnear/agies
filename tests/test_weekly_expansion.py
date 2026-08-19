"""Unit tests for Weekly Autonomous Expansion & GNN Predictive A&R Engine."""

from pathlib import Path
import tempfile

from agies.analytics.gnn_predictive import GNNPredictiveAREngine
from agies.graph.builder import MusicIndustryGraph
from agies.graph.schema import Artist, RelationshipEdge
from agies.orchestration.weekly_expansion import WeeklyKnowledgeGraphExpander


def test_gnn_predictive_ar_engine():
    graph = MusicIndustryGraph()

    # Add Artists
    a1 = Artist(id="art_1", name="Alpha Techno", genres=["Techno"])
    a2 = Artist(id="art_2", name="Beta Minimal", genres=["Techno"])
    a3 = Artist(
        id="art_emg_test",
        name="Gamma Breakout",
        genres=["Techno"],
        attributes={"development_tier": "Emerging Grassroots Artist"},
    )

    graph.add_entity(a1)
    graph.add_entity(a2)
    graph.add_entity(a3)

    graph.add_relationship(
        RelationshipEdge(
            source_id="art_1", target_id="art_2", rel_type="COLLABORATED_WITH"
        )
    )
    graph.add_relationship(
        RelationshipEdge(
            source_id="art_emg_test",
            target_id="art_1",
            rel_type="ACOUSTIC_SIMILARITY",
            weight=0.95,
        )
    )

    engine = GNNPredictiveAREngine(walk_length=5, num_walks=4, embedding_dim=16)
    embeddings = engine.fit_embeddings(graph)

    assert len(embeddings) == 3
    assert len(embeddings["art_1"]) == 16

    # Test Predictive Breakout A&R
    breakouts = engine.predict_breakout_ar_candidates(graph, top_k=2)
    assert len(breakouts) >= 1
    assert any(b["artist_id"] == "art_emg_test" for b in breakouts)


def test_weekly_knowledge_graph_expander_cycle():
    with tempfile.TemporaryDirectory() as tmpdir:
        expander = WeeklyKnowledgeGraphExpander(data_dir=Path(tmpdir))
        results = expander.run_weekly_cycle(target_audio_per_genre=5)

        assert results["total_nodes"] >= 400
        assert results["total_edges"] >= 1000
        assert results["audio_corpus_expansion"]["tracks_injected_to_graph"] >= 30
        assert Path(results["exported_cypher_file"]).exists()
        assert Path(results["exported_json_file"]).exists()
        assert len(results["predictive_breakout_artists"]) >= 1
