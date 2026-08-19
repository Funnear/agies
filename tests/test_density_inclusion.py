"""Unit tests for Graph Density Inclusion Engine."""

from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.density import GraphDensityInclusionEngine


def test_graph_density_inclusion_enrichment():
    graph = MusicIndustryGraph()
    c_ext = GlobalMusicIndustryCorpusExtractor()
    c_ent, c_edg = c_ext.extract()
    graph.ingest(c_ent, c_edg)

    initial_edges = len(graph.graph.edges)

    density_engine = GraphDensityInclusionEngine()
    results = density_engine.enrich_density(graph)

    assert results["total_nodes"] > 0
    assert results["total_edges"] > initial_edges
    assert results["graph_density"] > 0.0
    assert results["density_stats"]["hardware_nodes_added"] == 14
    assert results["density_stats"]["shared_studio_edges_added"] >= 0
    assert results["density_stats"]["label_mate_edges_added"] >= 0
