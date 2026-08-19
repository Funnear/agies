"""Unit tests for City-Level Industry Connects & Corridors."""

from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.hierarchy import GeoTaxonomyHierarchyBuilder
from agies.graph.city_connects import CityIndustryConnectsEnricher


def test_city_connects_enrichment():
    graph = MusicIndustryGraph()
    corp_ext = GlobalMusicIndustryCorpusExtractor()
    c_ent, c_edg = corp_ext.extract()
    graph.ingest(c_ent, c_edg)

    geo_b = GeoTaxonomyHierarchyBuilder()
    g_ent, g_edg = geo_b.build_hierarchy()
    graph.ingest(g_ent, g_edg)

    enricher = CityIndustryConnectsEnricher()
    res = enricher.enrich_city_connects(graph)

    assert res["city_anchors_added"] >= 40
    assert res["inter_city_corridors_added"] >= 8

    # Test City Profile for Berlin
    berlin_profile = enricher.get_city_profile(graph, "city_berlin")
    assert berlin_profile["city_name"] == "Berlin"
    assert berlin_profile["infrastructure_power_score"] > 20.0
    assert len(berlin_profile["studios"]) >= 2
    assert len(berlin_profile["record_labels"]) >= 2
    assert len(berlin_profile["inter_city_corridors"]) >= 1

    # Test City Profile for London
    london_profile = enricher.get_city_profile(graph, "city_london")
    assert london_profile["city_name"] == "London"
    assert len(london_profile["studios"]) >= 2
    assert len(london_profile["artists"]) >= 3
