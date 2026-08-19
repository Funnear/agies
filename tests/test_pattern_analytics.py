"""Unit tests for Behavioral Pattern Analytics Engine."""

import pytest
from agies.analytics.patterns import MusicIndustryAnalytics
from agies.graph.builder import MusicIndustryGraph
from agies.graph.extractors.synthetic_extractor import SyntheticIndustryExtractor


@pytest.fixture
def populated_graph():
    extractor = SyntheticIndustryExtractor()
    entities, edges = extractor.extract()
    graph = MusicIndustryGraph()
    graph.ingest(entities, edges)
    return graph


def test_power_brokers(populated_graph):
    analytics = MusicIndustryAnalytics(populated_graph)
    brokers = analytics.compute_power_brokers(top_k=5)

    assert "by_pagerank" in brokers
    assert "by_betweenness" in brokers
    assert len(brokers["by_pagerank"]) == 5
    assert len(brokers["by_betweenness"]) == 5

    # Scores should be positive and sorted descending
    pr_scores = [item["score"] for item in brokers["by_pagerank"]]
    assert pr_scores == sorted(pr_scores, reverse=True)


def test_creative_ecosystems(populated_graph):
    analytics = MusicIndustryAnalytics(populated_graph)
    ecosystems = analytics.detect_creative_ecosystems()

    assert len(ecosystems) > 1
    # Check community structure
    first_comm = ecosystems[0]
    assert "community_id" in first_comm
    assert "size" in first_comm
    assert first_comm["size"] > 1
    assert "entity_composition" in first_comm


def test_label_mobility_analysis(populated_graph):
    analytics = MusicIndustryAnalytics(populated_graph)
    mobility = analytics.analyze_label_mobility()

    assert mobility["total_artists_analyzed"] > 10
    assert mobility["loyal_count"] > 0
    assert mobility["migrated_count"] > 0
    assert mobility["migration_rate_percentage"] > 0.0

    # Ensure migrating artists have past labels
    migrated_names = [a["artist_name"] for a in mobility["migrated_artists"]]
    assert "Taylor Swift" in migrated_names
    assert "Drake" in migrated_names


def test_studio_reliance_index(populated_graph):
    analytics = MusicIndustryAnalytics(populated_graph)
    spri = analytics.compute_studio_reliance()

    assert len(spri) > 10
    for record in spri:
        assert "reliance_index" in record
        assert 0.0 <= record["reliance_index"] <= 1.0


def test_agency_collaboration_density(populated_graph):
    analytics = MusicIndustryAnalytics(populated_graph)
    density = analytics.analyze_agency_collaboration_density()

    assert "total_collaborations" in density
    assert density["total_collaborations"] > 0
    assert "intra_agency_collaborations" in density
    assert "inter_agency_collaborations" in density
    assert "behavior_interpretation" in density
