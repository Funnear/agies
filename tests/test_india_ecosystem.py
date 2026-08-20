"""Unit tests for India Music Ecosystem and Mumbai Ground Zero Ingestion."""

from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.india_ecosystem import IndiaMusicEcosystemBuilder


def test_india_ecosystem_enrichment():
    graph = MusicIndustryGraph()
    c_ext = GlobalMusicIndustryCorpusExtractor()
    c_ent, c_edg = c_ext.extract()
    graph.ingest(c_ent, c_edg)

    initial_nodes = len(graph.graph.nodes)

    builder = IndiaMusicEcosystemBuilder()
    stats = builder.enrich_india_ecosystem(graph)

    assert stats["cities_added"] >= 4
    assert stats["venues_added"] >= 8
    assert stats["studios_added"] >= 3
    assert stats["labels_collectives_added"] >= 4
    assert stats["artists_added"] >= 5
    assert len(graph.graph.nodes) > initial_nodes

    # Check Mumbai ground zero entities
    assert "city_mumbai" in graph.graph
    assert "ven_antisocial_mumbai" in graph.graph
    assert "ven_bonobo_mumbai" in graph.graph
    assert "std_yrf_mumbai" in graph.graph
    assert "std_islandcity_mumbai" in graph.graph
    assert "lbl_azadi_records" in graph.graph
    assert "lbl_gully_gang" in graph.graph
    assert "coll_boxout_fm" in graph.graph
    assert "art_divine" in graph.graph
    assert "art_sandunes" in graph.graph

    # Check regional hubs
    assert "city_goa" in graph.graph
    assert "ven_hilltop_goa" in graph.graph
    assert "city_bengaluru" in graph.graph
    assert "ven_fandom_bengaluru" in graph.graph
    assert "city_delhi" in graph.graph
    assert "art_seedhe_maut" in graph.graph
    assert "city_chennai" in graph.graph
    assert "std_panchathan_chennai" in graph.graph
    assert "art_ar_rahman" in graph.graph
