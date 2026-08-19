"""Venue Discovery & Artist Booking API Router."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from agies.api.auth import APIKeyInfo, get_api_key
from agies.graph.builder import MusicIndustryGraph
from agies.graph.corpus import GlobalMusicIndustryCorpusExtractor
from agies.graph.micro_corpus import MicroEcosystemCorpusExtractor
from agies.graph.hierarchy import GeoTaxonomyHierarchyBuilder
from agies.graph.city_connects import CityIndustryConnectsEnricher
from agies.graph.enrichment import AcousticGraphEnricher
from agies.venues.corpus import VenueCorpus
from agies.venues.discovery import VenueArtistDiscoveryEngine
from agies.venues.models import (
    ArtistVenueMatch,
    BookingContactCard,
    BookingInquiryReceipt,
    BookingInquiryRequest,
    Venue,
    VenueCapacityTier,
)

router = APIRouter(prefix="/venues", tags=["Venues & Artist Booking"])

# Shared graph instance initialized with full ecosystem
_graph_instance = MusicIndustryGraph()
_c_ext = GlobalMusicIndustryCorpusExtractor()
_c_ent, _c_edg = _c_ext.extract()
_graph_instance.ingest(_c_ent, _c_edg)

_m_ext = MicroEcosystemCorpusExtractor()
_m_ent, _m_edg = _m_ext.extract()
_graph_instance.ingest(_m_ent, _m_edg)

_g_b = GeoTaxonomyHierarchyBuilder()
_g_ent, _g_edg = _g_b.build_hierarchy()
_graph_instance.ingest(_g_ent, _g_edg)

_city_enr = CityIndustryConnectsEnricher()
_city_enr.enrich_city_connects(_graph_instance)

_enricher = AcousticGraphEnricher()
_enricher.enrich_graph(_graph_instance)

_discovery_engine = VenueArtistDiscoveryEngine(industry_graph=_graph_instance)


class CustomVenueProfileRequest(BaseModel):
    name: str = Field(description="Venue or event name")
    city: str = Field(description="City location")
    country: str = Field(default="Germany", description="Country")
    capacity: int = Field(default=500, description="Venue audience capacity")
    genres: List[str] = Field(
        default=["Techno", "Electronic"], description="Target programming genres"
    )


@router.get("/list", summary="Browse music venues and club landmarks")
async def list_venues(
    city: Optional[str] = Query(
        None, description="Filter by city (e.g. Berlin, London, New York City, Paris)"
    ),
    tier: Optional[str] = Query(
        None, description="Filter by capacity tier: intimate, club, hall, arena"
    ),
    key: APIKeyInfo = Depends(get_api_key),
) -> List[Venue]:
    """Retrieve catalog of world-class and grassroots music venues."""
    return VenueCorpus.list_venues(city=city, tier=tier)


@router.get(
    "/recommend-artists/{venue_id}",
    summary="Find matching artists for a specific venue",
)
async def recommend_artists_for_venue(
    venue_id: str,
    top_k: int = Query(10, ge=1, le=30, description="Number of artists to recommend"),
    key: APIKeyInfo = Depends(get_api_key),
) -> List[ArtistVenueMatch]:
    """Match emerging and touring artists to a venue based on acoustic profile, BPM, and capacity fit."""
    venue = VenueCorpus.get_venue(venue_id)
    if not venue:
        raise HTTPException(
            status_code=404, detail=f"Venue '{venue_id}' not found in directory."
        )

    return _discovery_engine.discover_artists_for_venue(venue=venue, top_k=top_k)


@router.post("/recommend-by-profile", summary="Find artists for a custom venue profile")
async def recommend_artists_by_profile(
    request: CustomVenueProfileRequest,
    top_k: int = Query(10, ge=1, le=30),
    key: APIKeyInfo = Depends(get_api_key),
) -> List[ArtistVenueMatch]:
    """Match artists to any custom venue configuration."""
    cap_tier = (
        VenueCapacityTier.INTIMATE
        if request.capacity <= 250
        else (
            VenueCapacityTier.CLUB
            if request.capacity <= 800
            else (
                VenueCapacityTier.HALL
                if request.capacity <= 2500
                else VenueCapacityTier.ARENA
            )
        )
    )
    temp_venue = Venue(
        id="custom_venue",
        name=request.name,
        city=request.city,
        country=request.country,
        capacity=request.capacity,
        capacity_tier=cap_tier,
        genres=request.genres,
        booking_email="promoter@custom.venue",
    )
    return _discovery_engine.discover_artists_for_venue(venue=temp_venue, top_k=top_k)


@router.get(
    "/support-acts/{headliner_id}",
    summary="Recommend opening and support acts for a headliner",
)
async def recommend_support_acts(
    headliner_id: str,
    venue_capacity: int = Query(500, description="Venue audience capacity"),
    top_k: int = Query(5, ge=1, le=15),
    key: APIKeyInfo = Depends(get_api_key),
) -> List[ArtistVenueMatch]:
    """Recommend complementary opening acts tailored to a headliner's acoustic vibe."""
    return _discovery_engine.recommend_support_acts(
        headliner_id=headliner_id, venue_capacity=venue_capacity, top_k=top_k
    )


@router.get(
    "/contact/{artist_id}", summary="Get direct booking and management contact card"
)
async def get_artist_booking_contact(
    artist_id: str,
    key: APIKeyInfo = Depends(get_api_key),
) -> BookingContactCard:
    """Retrieve primary booking agency, management contact, and direct email for an artist."""
    return _discovery_engine.get_booking_contact(artist_id=artist_id)


@router.post(
    "/inquire", summary="Dispatch structured booking inquiry to artist representative"
)
async def submit_booking_inquiry(
    request: BookingInquiryRequest,
    key: APIKeyInfo = Depends(get_api_key),
) -> BookingInquiryReceipt:
    """Submit a formal booking offer to an artist's booking agent or management team."""
    try:
        return _discovery_engine.create_booking_inquiry(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inquiry dispatch failed: {e}")
