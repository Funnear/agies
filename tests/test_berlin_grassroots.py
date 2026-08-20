"""Unit tests for Berlin Grassroots Underground Ecosystem and Live Audio Harvester."""

from agies.audio.grassroots_scraper import BerlinGrassrootsAudioHarvester
from agies.graph.berlin_grassroots import BerlinGrassrootsEcosystemBuilder
from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor


def test_berlin_grassroots_enrichment():
    graph = MusicIndustryGraph()
    c_ext = GlobalMusicIndustryCorpusExtractor()
    c_ent, c_edg = c_ext.extract()
    graph.ingest(c_ent, c_edg)

    initial_nodes = len(graph.graph.nodes)

    builder = BerlinGrassrootsEcosystemBuilder()
    stats = builder.enrich_berlin_grassroots(graph)

    assert stats["venues_added"] >= 10
    assert stats["collectives_added"] >= 5
    assert stats["radios_added"] >= 3
    assert stats["record_stores_added"] >= 4
    assert stats["grassroots_audio_snippets_added"] >= 5
    assert len(graph.graph.nodes) > initial_nodes

    # Check key Berlin grassroots clubs and collectives
    assert "ven_sisyphos" in graph.graph
    assert "ven_rso" in graph.graph
    assert "ven_about_blank" in graph.graph
    assert "coll_herrensauna" in graph.graph
    assert "coll_malajunta" in graph.graph
    assert "radio_hoer" in graph.graph
    assert "store_hardwax" in graph.graph


def test_berlin_grassroots_audio_harvester(tmp_path):
    harvester = BerlinGrassrootsAudioHarvester(snippets_dir=tmp_path / "snippets")
    files = harvester.harvest_all_grassroots_audio()

    assert len(files) >= 5
    for f in files:
        assert f.exists()
        assert f.stat().st_size > 1000
