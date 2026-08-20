from agies.graph.berlin_grassroots import BerlinGrassrootsEcosystemBuilder
from agies.graph.builder import MusicIndustryGraph
from agies.graph.city_connects import CityIndustryConnectsEnricher
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.hierarchy import GeoTaxonomyHierarchyBuilder
from agies.graph.wavefront_expansion import ConcentricGeographicWaveFrontExpander
from agies.search.graph_search_engine import EfficientGraphSearchEngine


def test_efficient_graph_search_engine():
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
    wave_engine.expand_concentric_wavefront(graph, max_wave=3)

    search_engine = EfficientGraphSearchEngine(graph)

    # 1. Inverted Index Search
    results = search_engine.search_entities("Berlin")
    assert len(results) > 0
    assert any("berlin" in r.name.lower() or "berlin" in r.entity_id.lower() for r in results)

    # 2. Pruned Beam Search Subcultural Cluster
    cluster = search_engine.beam_search_subcultural_cluster("city_berlin", beam_width=4, max_depth=2)
    assert len(cluster) >= 4
    for item in cluster:
        assert item.score > 0
        assert item.path_trail is not None

    # 3. A* Harmonic Shortest Pathfinding
    path_res = search_engine.find_shortest_harmonic_path("city_berlin", "city_leipzig")
    assert path_res is not None
    assert "path" in path_res
    assert len(path_res["path"]) >= 2
    assert path_res["path"][0] == "city_berlin"
    assert path_res["path"][-1] == "city_leipzig"
