"""Unit tests for Advanced Analytics, Structural Holes, and Link Prediction."""

import pytest
from agies.analytics.advanced import AdvancedIndustryAnalytics
from agies.graph.builder import MusicIndustryGraph
from agies.graph.extractors.synthetic_extractor import SyntheticIndustryExtractor


@pytest.fixture
def populated_graph():
    extractor = SyntheticIndustryExtractor()
    entities, edges = extractor.extract()
    graph = MusicIndustryGraph()
    graph.ingest(entities, edges)
    return graph


def test_structural_holes_analysis(populated_graph):
    analytics = AdvancedIndustryAnalytics(populated_graph)
    brokers = analytics.analyze_structural_holes(top_k=5)

    assert len(brokers) == 5
    for b in brokers:
        assert "network_constraint" in b
        assert "brokerage_potential" in b
        assert b["network_constraint"] > 0


def test_k_core_decomposition(populated_graph):
    analytics = AdvancedIndustryAnalytics(populated_graph)
    k_core = analytics.compute_k_core_decomposition()

    assert k_core["max_core_level"] >= 1
    assert "core_breakdown" in k_core
    assert len(k_core["core_breakdown"]) > 0


def test_collaboration_predictions(populated_graph):
    analytics = AdvancedIndustryAnalytics(populated_graph)
    predictions = analytics.predict_future_collaborations(top_k=5)

    assert len(predictions) > 0
    first = predictions[0]
    assert "artist_1" in first
    assert "artist_2" in first
    assert "affinity_score" in first
    assert first["affinity_score"] > 0
    assert first["likelihood"] in ("Very High", "High", "Moderate")


def test_era_evolution(populated_graph):
    analytics = AdvancedIndustryAnalytics(populated_graph)
    eras = analytics.analyze_era_evolution()

    assert "Early_Eras (<=2009)" in eras
    assert "Streaming_Rise (2010-2019)" in eras
    assert "Modern_Ecosystem (2020+)" in eras
