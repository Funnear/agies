"""Entity-Relationship Schema for the Music Industry Knowledge Graph."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    """Entity types in the music industry ecosystem."""

    ARTIST = "artist"
    RECORD_LABEL = "record_label"
    PRODUCTION_HOUSE = "production_house"
    AGENCY = "agency"  # Booking / Management / Talent agency
    STUDIO = "studio"  # Recording / Mastering studio
    PRODUCER = "producer"  # Music producer / Sound engineer
    RELEASE = "release"  # Album / EP / Single
    TRACK = "track"  # Individual song


class RelationshipType(str, Enum):
    """Relationship / Edge types connecting industry entities."""

    SIGNED_TO = "SIGNED_TO"  # Artist -> RecordLabel / ProductionHouse
    REPRESENTED_BY = "REPRESENTED_BY"  # Artist -> Agency
    RECORDED_AT = "RECORDED_AT"  # Artist / Release -> Studio
    PRODUCED_BY = "PRODUCED_BY"  # Track / Release / Artist -> Producer
    COLLABORATED_WITH = "COLLABORATED_WITH"  # Artist -> Artist
    PARENT_COMPANY_OF = "PARENT_COMPANY_OF"  # Media Conglomerate -> Label / Agency
    DISTRIBUTED_BY = "DISTRIBUTED_BY"  # Label / Release -> Distributor
    FEATURED_ON = "FEATURED_ON"  # Track -> Release / Curation
    SHOWCASED_AT = "SHOWCASED_AT"  # Artist -> ShowcaseFestival
    COLLECTS_ROYALTIES_VIA = "COLLECTS_ROYALTIES_VIA"  # Artist -> RightsOrganization
    A_AND_R_PIPELINE = "A_AND_R_PIPELINE"  # Grassroots -> Major Label / Agency
    CLASSIFIED_AS_GENRE = "CLASSIFIED_AS_GENRE"  # Artist -> Genre
    ACOUSTIC_SIMILARITY = "ACOUSTIC_SIMILARITY"  # Artist <-> Artist


class BaseEntity(BaseModel):
    """Base graph node entity."""

    id: str
    name: str
    entity_type: EntityType
    country: Optional[str] = None
    genres: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)


class Artist(BaseEntity):
    """Artist or Band entity."""

    entity_type: EntityType = EntityType.ARTIST
    type: str = Field(default="Person", description="Person or Group")
    active_since: Optional[int] = None
    is_active: bool = True


class RecordLabel(BaseEntity):
    """Record Label or Production House entity."""

    entity_type: EntityType = EntityType.RECORD_LABEL
    is_major: bool = False
    parent_company: Optional[str] = None
    founded_year: Optional[int] = None


class ProductionHouse(BaseEntity):
    """Music Production House entity."""

    entity_type: EntityType = EntityType.PRODUCTION_HOUSE
    specialties: List[str] = Field(default_factory=list)


class Agency(BaseEntity):
    """Management, Booking, or Talent Agency."""

    entity_type: EntityType = EntityType.AGENCY
    agency_type: str = Field(
        default="Management", description="Management, Booking, or PR"
    )


class Studio(BaseEntity):
    """Recording, Mixing, or Mastering Studio."""

    entity_type: EntityType = EntityType.STUDIO
    city: Optional[str] = None
    equipment_tier: Optional[str] = None


class Producer(BaseEntity):
    """Producer, Composer, or Sound Engineer."""

    entity_type: EntityType = EntityType.PRODUCER
    role: str = Field(
        default="Executive Producer", description="Producer, Mix Engineer, Mastering"
    )


class Release(BaseEntity):
    """Album, EP, or Single release."""

    entity_type: EntityType = EntityType.RELEASE
    release_year: Optional[int] = None
    release_type: str = "Album"  # Album, EP, Single


class Track(BaseEntity):
    """Individual audio track."""

    entity_type: EntityType = EntityType.TRACK
    duration_seconds: Optional[float] = None
    isrc: Optional[str] = None


class RelationshipEdge(BaseModel):
    """Directed relationship edge between two entities."""

    source_id: str
    target_id: str
    rel_type: RelationshipType
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    weight: float = Field(
        default=1.0, description="Strength or frequency of relationship"
    )
    is_current: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
