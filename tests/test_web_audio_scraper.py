"""Unit tests for Web Audio Scraper & Knowledge Graph Enrichment."""

from agies.audio.web_audio_scraper import WebAudioScraperEnricher
from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor


def test_web_audio_scraper_enrichment(tmp_path):
    graph = MusicIndustryGraph()
    c_ext = GlobalMusicIndustryCorpusExtractor()
    c_ent, c_edg = c_ext.extract()
    graph.ingest(c_ent, c_edg)

    initial_nodes = len(graph.graph.nodes)
    initial_edges = len(graph.graph.edges)

    scraper = WebAudioScraperEnricher(cache_dir=tmp_path / "cache", snippets_dir=tmp_path / "snippets")
    results = scraper.scrape_and_enrich_all(graph)

    assert results["scraped_tracks_count"] > 0
    assert results["scraped_gear_count"] > 0
    assert len(graph.graph.nodes) > initial_nodes
    assert len(graph.graph.edges) > initial_edges
    assert (tmp_path / "cache" / "scraped_audio_corpus.json").exists()
