"""Unit tests for Global Curator Scraper (Anjuna, Boiler Room, Cercle, Afterlife, Keinemusik)."""

from agies.audio.curator_scraper import GlobalCuratorWebScraperEnricher
from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.india_ecosystem import IndiaMusicEcosystemBuilder


def test_global_curator_scraper(tmp_path):
    graph = MusicIndustryGraph()
    c_ext = GlobalMusicIndustryCorpusExtractor()
    c_ent, c_edg = c_ext.extract()
    graph.ingest(c_ent, c_edg)

    india_builder = IndiaMusicEcosystemBuilder()
    india_builder.enrich_india_ecosystem(graph)

    initial_nodes = len(graph.graph.nodes)

    scraper = GlobalCuratorWebScraperEnricher(snippets_dir=tmp_path / "curator_snippets")
    stats = scraper.scrape_and_enrich_curators(graph)

    assert stats["curator_sessions_added"] >= 5
    assert stats["curator_edges_added"] >= 5
    assert stats["audio_snippets_generated"] >= 5
    assert len(graph.graph.nodes) > initial_nodes

    # Check key curator broadcast sessions
    assert "cur_anjuna_goa_sunset" in graph.graph
    assert "cur_boiler_room_anjuna" in graph.graph
    assert "cur_boiler_room_mumbai" in graph.graph
    assert "cur_cercle_bodzin_colosseum" in graph.graph
    assert "cur_afterlife_tulum_zamna" in graph.graph
    assert "cur_keinemusik_pyramids_giza" in graph.graph
