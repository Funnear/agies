"""Unit tests for Weekly Autonomous Expansion & GNN Predictive A&R Engine."""

from pathlib import Path
import tempfile

from agies.analytics.gnn_predictive import GNNPredictiveAREngine
from agies.graph.builder import MusicIndustryGraph
from agies.graph.schema import Artist, RelationshipEdge
from agies.orchestration.autonomous_expansion import AutonomousKnowledgeGraphExpander


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
    breakouts = engine.predict_breakout_ar_candidates(graph, top_k=2)
    assert len(breakouts) >= 1


def test_autonomous_expansion_orchestrator():
    with tempfile.TemporaryDirectory() as tmpdir:
        expander = AutonomousKnowledgeGraphExpander(data_dir=Path(tmpdir))
        results = expander.run_autonomous_cycle(target_audio_per_genre=5)

        assert results["total_nodes"] > 0
        assert results["total_edges"] > 0
        assert "predictive_breakout_artists" in results
        assert Path(results["exported_cypher_file"]).exists()
        assert Path(results["exported_json_file"]).exists()
        assert len(results["predictive_breakout_artists"]) >= 1
