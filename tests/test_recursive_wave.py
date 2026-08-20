"""Unit tests for Recursive Multi-Hop Wave Propagation Engine."""

from agies.graph.berlin_grassroots import BerlinGrassrootsEcosystemBuilder
from agies.graph.builder import MusicIndustryGraph
from agies.graph.city_connects import CityIndustryConnectsEnricher
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.hierarchy import GeoTaxonomyHierarchyBuilder
from agies.graph.recursive_wave import RecursiveWavePropagationEngine
from agies.graph.wavefront_expansion import ConcentricGeographicWaveFrontExpander


def test_recursive_wave_propagation():
    graph = MusicIndustryGraph()
    c_ext = GlobalMusicIndustryCorpusExtractor()
    c_ent, c_edg = c_ext.extract()
    graph.ingest(c_ent, c_edg)

    geo_b = GeoTaxonomyHierarchyBuilder()
    g_ent, g_edg = geo_b.build_hierarchy()
    graph.ingest(g_ent, g_edg)

    city_enr = CityIndustryConnectsEnricher()
    city_enr.enrich_city_connects(graph)

    berlin_builder = BerlinGrassrootsEcosystemBuilder()
    berlin_builder.enrich_berlin_grassroots(graph)

    wave_engine = ConcentricGeographicWaveFrontExpander()
    wave_engine.expand_concentric_wavefront(graph, max_wave=2)

    initial_nodes = len(graph.graph.nodes)
    initial_edges = len(graph.graph.edges)

    engine = RecursiveWavePropagationEngine()
    stats = engine.recurse_graph_waves(graph, max_propagation_depth=3)

    assert stats["new_entities_added"] >= 5
    assert stats["new_transitive_edges_added"] >= 10
    assert stats["max_propagation_depth_executed"] >= 2
    assert len(graph.graph.nodes) > initial_nodes
    assert len(graph.graph.edges) > initial_edges

    # Verify satellite feeder micro-hubs spawned through recursive node traversal
    assert "ven_potsdam_fabrik" in graph.graph
    assert "coll_brandenburg_ambient" in graph.graph
    assert "ven_conne_island" in graph.graph
    assert "store_tief_leipzig" in graph.graph
    assert "ven_ot301_ams" in graph.graph
