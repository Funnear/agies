"""Unit tests for Concentric Wave-Front Global Expansion Engine."""

from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.wavefront_expansion import ConcentricGeographicWaveFrontExpander


def test_concentric_wavefront_expansion():
    graph = MusicIndustryGraph()
    c_ext = GlobalMusicIndustryCorpusExtractor()
    c_ent, c_edg = c_ext.extract()
    graph.ingest(c_ent, c_edg)

    initial_nodes = len(graph.graph.nodes)

    engine = ConcentricGeographicWaveFrontExpander()
    stats = engine.expand_concentric_wavefront(graph, max_wave=3)

    assert stats["cities_added"] >= 5
    assert stats["venues_added"] >= 15
    assert stats["collectives_added"] >= 5
    assert stats["record_stores_added"] >= 5
    assert stats["intercity_corridor_edges_added"] >= 5
    assert len(graph.graph.nodes) > initial_nodes

    # Check key neighbor hubs across the concentric wave rings
    # Wave 1 (German / Central European neighbor ring)
    assert "city_leipzig" in graph.graph
    assert "ven_ifz_leipzig" in graph.graph
    assert "city_hamburg" in graph.graph
    assert "ven_pudel_hamburg" in graph.graph
    assert "city_prague" in graph.graph
    assert "ven_ankali_prague" in graph.graph
    assert "city_cologne" in graph.graph
    assert "ven_salon_des_amateurs" in graph.graph
    assert "city_frankfurt" in graph.graph
    assert "ven_robert_johnson" in graph.graph
    assert "city_munich" in graph.graph
    assert "ven_blitz_munich" in graph.graph

    # Wave 2 (Western & Northern European sister ring)
    assert "city_amsterdam" in graph.graph
    assert "ven_shelter_amsterdam" in graph.graph
    assert "city_brussels" in graph.graph
    assert "ven_fuse_brussels" in graph.graph
    assert "city_zurich" in graph.graph
    assert "ven_elysia_basel" in graph.graph

    # Wave 3 (Mediterranean & Caucasus Axis)
    assert "city_tbilisi" in graph.graph
    assert "ven_bassiani_tbilisi" in graph.graph
    assert "city_barcelona" in graph.graph
    assert "ven_nitsa_bcn" in graph.graph
    assert "city_lisbon" in graph.graph
    assert "ven_lux_lisbon" in graph.graph
