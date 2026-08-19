"""Unit tests for Bedroom Producer Assistant and Demo Diagnostic Engine."""

from agies.audio.bedroom_producer import BedroomProducerAssistant, DemoAnalysisReport
from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.micro_corpus import MicroEcosystemCorpusExtractor


def test_bedroom_producer_assistant_generation():
    graph = MusicIndustryGraph()
    c_ent, c_edg = GlobalMusicIndustryCorpusExtractor().extract()
    graph.ingest(c_ent, c_edg)
    m_ent, m_edg = MicroEcosystemCorpusExtractor().extract()
    graph.ingest(m_ent, m_edg)

    assistant = BedroomProducerAssistant(industry_graph=graph)

    report = assistant.analyze_demo_and_generate_dossier(
        track_title="Subterranean Frequency",
        artist_name="Klangwerk Beta",
        home_city="Berlin",
        home_country="Germany",
        subgenre_hint="Techno",
    )

    assert isinstance(report, DemoAnalysisReport)
    assert report.artist_name == "Klangwerk Beta"
    assert report.detected_bpm > 100
    assert len(report.nearest_acoustic_artist_matches) >= 1
    assert len(report.recommended_debut_venues) >= 1
    assert any("Phase 1" in k for k in report.four_phase_roadmap)
    assert "Klangwerk Beta" in report.generated_booking_pitch
    assert "Berlin" in report.generated_booking_pitch
