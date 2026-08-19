"""Venue Models, Booking Contact Cards, and Inquiries Schema."""

from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class VenueCapacityTier(str, Enum):
    """Venue capacity categories."""

    INTIMATE = "intimate"  # 50 - 250 capacity (Grassroots stepping-stone)
    CLUB = "club"  # 250 - 800 capacity (Mid-size club / showcase venue)
    HALL = "hall"  # 800 - 2,500 capacity (Concert hall / theatre)
    ARENA = "arena"  # 2,500+ capacity (Major arena / festival stage)


class Venue(BaseModel):
    """Music Venue node profile."""

    id: str
    name: str
    city: str
    country: str
    capacity: int
    capacity_tier: VenueCapacityTier
    genres: List[str] = Field(default_factory=list)
    sound_system: Optional[str] = "Funktion-One / L-Acoustics"
    booking_email: str
    description: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)


class BookingContactCard(BaseModel):
    """Direct booking and management contact information for an artist."""

    artist_id: str
    artist_name: str
    representation_type: str  # 'Agency Representation' or 'Self-Managed / Direct'
    primary_booking_agent: Optional[str] = None
    agency_name: Optional[str] = None
    booking_email: str
    management_contact: Optional[str] = None
    territory_coverage: str = "Global / Worldwide"
    preferred_inquiry_notice_weeks: int = 4
    standard_fee_range: str = "Inquire for quote"


class BookingInquiryRequest(BaseModel):
    """Structured booking inquiry submitted by a venue or promoter."""

    venue_id: str
    venue_name: str
    artist_id: str
    event_date: date
    offer_fee_currency: str = "EUR"
    offer_fee_amount: float
    set_type: str = "Live Set (60-90 min)"  # 'Live Set', 'DJ Set', 'Opening Support'
    expected_attendance: int
    promoter_name: str
    promoter_email: str
    special_notes: Optional[str] = None


class BookingInquiryReceipt(BaseModel):
    """Confirmation receipt of a dispatched booking inquiry."""

    inquiry_id: str
    status: str = "dispatched"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    recipient_email: str
    artist_name: str
    venue_name: str
    offer_fee: str
    next_steps: str


class ArtistVenueMatch(BaseModel):
    """Recommended artist match tailored to a venue's acoustic profile and capacity."""

    artist_id: str
    artist_name: str
    classified_subgenre: str
    detected_bpm: float
    match_score: float  # 0.0 - 1.0
    capacity_fit: str  # 'Optimal Headliner', 'Emerging Support Act', 'Breakout Debut'
    development_tier: str
    booking_agency: Optional[str] = None
    direct_contact_available: bool = True
    match_rationale: str
