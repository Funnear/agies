"""Unit tests for Entity Description & Context Enrichment Engine."""

from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.descriptions import EntityDescriptionEnricher


def test_entity_description_enrichment():
    graph = MusicIndustryGraph()
    c_ext = GlobalMusicIndustryCorpusExtractor()
    c_ent, c_edg = c_ext.extract()
    graph.ingest(c_ent, c_edg)

    enricher = EntityDescriptionEnricher()
    results = enricher.enrich_descriptions(graph)

    assert results["total_nodes_enriched"] > 0
    assert results["total_graph_nodes"] == len(graph.graph.nodes)

    # Verify specific nodes have authoritative descriptions
    for nid, data in graph.graph.nodes(data=True):
        assert "description" in data
        assert len(data["description"]) > 10
