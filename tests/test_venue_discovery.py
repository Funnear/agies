"""Unit tests for Venue Discovery, Artist Matchmaking, and Direct Booking Connection Engine."""

from datetime import date
import pytest

from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.micro_corpus import MicroEcosystemCorpusExtractor
from agies.graph.hierarchy import GeoTaxonomyHierarchyBuilder
from agies.graph.enrichment import AcousticGraphEnricher
from agies.venues.corpus import VenueCorpus
from agies.venues.discovery import VenueArtistDiscoveryEngine
from agies.venues.models import BookingInquiryRequest


@pytest.fixture
def venue_engine():
    graph = MusicIndustryGraph()
    c_ent, c_edg = GlobalMusicIndustryCorpusExtractor().extract()
    graph.ingest(c_ent, c_edg)
    m_ent, m_edg = MicroEcosystemCorpusExtractor().extract()
    graph.ingest(m_ent, m_edg)
    g_ent, g_edg = GeoTaxonomyHierarchyBuilder().build_hierarchy()
    graph.ingest(g_ent, g_edg)
    AcousticGraphEnricher().enrich_graph(graph)

    return VenueArtistDiscoveryEngine(industry_graph=graph)


def test_venue_corpus_lookup():
    berghain = VenueCorpus.get_venue("ven_berghain")
    assert berghain is not None
    assert berghain.city == "Berlin"
    assert berghain.capacity == 1500
    assert "Techno" in berghain.genres

    london_venues = VenueCorpus.list_venues(city="London")
    assert len(london_venues) >= 2


def test_discover_artists_for_berghain(venue_engine):
    berghain = VenueCorpus.get_venue("ven_berghain")
    matches = venue_engine.discover_artists_for_venue(venue=berghain, top_k=5)

    assert len(matches) >= 1
    assert matches[0].match_score > 0.70
    assert matches[0].direct_contact_available is True
    # Verify acoustic metadata
    assert matches[0].detected_bpm > 0


def test_recommend_support_acts(venue_engine):
    # Recommend support acts for Stephan Bodzin
    supports = venue_engine.recommend_support_acts(
        headliner_id="art_stephanbodzin_art", venue_capacity=800, top_k=3
    )
    assert len(supports) >= 1
    assert supports[0].capacity_fit == "Opening Support Act"


def test_booking_contact_resolution(venue_engine):
    # 1. Agency Represented Artist (e.g. Kraftwerk -> Primary Talent)
    contact_agency = venue_engine.get_booking_contact("art_kraftwerk")
    assert contact_agency.artist_name == "Kraftwerk"
    assert "@" in contact_agency.booking_email

    # 2. Emerging Artist (e.g. Klangformer)
    contact_emerging = venue_engine.get_booking_contact("art_emg_berlin_tech")
    assert contact_emerging.artist_id == "art_emg_berlin_tech"
    assert "@" in contact_emerging.booking_email


def test_create_booking_inquiry(venue_engine):
    inquiry = BookingInquiryRequest(
        venue_id="ven_tresor",
        venue_name="Tresor Berlin",
        artist_id="art_emg_berlin_tech",
        event_date=date(2026, 11, 14),
        offer_fee_currency="EUR",
        offer_fee_amount=1200.00,
        set_type="Live Club Set (90 min)",
        expected_attendance=600,
        promoter_name="Tresor Bookings Team",
        promoter_email="programming@tresorberlin.com",
        special_notes="Headlining the Globus floor with direct support.",
    )

    receipt = venue_engine.create_booking_inquiry(inquiry)
    assert receipt.inquiry_id.startswith("inq_")
    assert receipt.status == "dispatched"
    assert "Tresor Berlin" in receipt.venue_name
    assert "1,200.00 EUR" in receipt.offer_fee
