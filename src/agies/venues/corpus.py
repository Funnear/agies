"""Global Venue Catalog & Grassroots Venue Corpus."""

from typing import List, Optional
from agies.venues.models import Venue, VenueCapacityTier


class VenueCorpus:
    """Directory of global iconic venues, club landmarks, and grassroots stepping-stone spaces."""

    VENUES: List[Venue] = [
        # === BERLIN ===
        Venue(
            id="ven_berghain",
            name="Berghain / Panorama Bar",
            city="Berlin",
            country="Germany",
            capacity=1500,
            capacity_tier=VenueCapacityTier.HALL,
            genres=["Techno", "Industrial", "House"],
            sound_system="Funktion-One Custom (Double 21-inch Subs)",
            booking_email="booking@berghain.de",
            description="The world's foremost temple of techno and club culture.",
        ),
        Venue(
            id="ven_tresor",
            name="Tresor Berlin",
            city="Berlin",
            country="Germany",
            capacity=800,
            capacity_tier=VenueCapacityTier.CLUB,
            genres=["Techno", "Detroit Techno", "Electro"],
            sound_system="Funktion-One Vault Acoustics",
            booking_email="booking@tresorberlin.com",
            description="Historic power plant vault and underground techno institution.",
        ),
        Venue(
            id="ven_gretchen",
            name="Club Gretchen",
            city="Berlin",
            country="Germany",
            capacity=600,
            capacity_tier=VenueCapacityTier.CLUB,
            genres=["Drum and Bass", "Bass", "Hip-Hop", "Neo-Soul"],
            sound_system="L-Acoustics Kiva",
            booking_email="booking@gretchen-club.de",
            description="Leading venue for bass music, broken beats, and live electronic acts.",
        ),
        Venue(
            id="ven_funkhaus_saal",
            name="Funkhaus Berlin (Saal 1)",
            city="Berlin",
            country="Germany",
            capacity=2200,
            capacity_tier=VenueCapacityTier.HALL,
            genres=["Neo-Classical", "Ambient", "Orchestral", "Experimental"],
            sound_system="Custom Acoustic Diffusion Panels & D&B Audiotechnik",
            booking_email="events@funkhaus-berlin.net",
            description="World's largest historic acoustic recording hall and live showcase space.",
        ),
        Venue(
            id="ven_schokoladen",
            name="Schokoladen (Mitte)",
            city="Berlin",
            country="Germany",
            capacity=150,
            capacity_tier=VenueCapacityTier.INTIMATE,
            genres=["Indie Rock", "Post-Punk", "Bedroom Pop"],
            sound_system="Vintage Analog PA",
            booking_email="booking@schokoladen-mitte.de",
            description="Grassroots stepping-stone venue in Berlin-Mitte for debut artists.",
        ),
        # === LONDON ===
        Venue(
            id="ven_fabric",
            name="Fabric London",
            city="London",
            country="United Kingdom",
            capacity=1600,
            capacity_tier=VenueCapacityTier.HALL,
            genres=["Techno", "House", "Drum and Bass", "UK Garage"],
            sound_system="Pioneer Pro Audio Bodysonic Bass Floor",
            booking_email="programming@fabriclondon.com",
            description="Iconic multi-room electronic and club music benchmark.",
        ),
        Venue(
            id="ven_village_underground",
            name="Village Underground",
            city="London",
            country="United Kingdom",
            capacity=720,
            capacity_tier=VenueCapacityTier.CLUB,
            genres=["Electronic", "Indie Rock", "Afro-Fusion", "Neo-Soul"],
            sound_system="d&b audiotechnik V-Series",
            booking_email="music@villageunderground.co.uk",
            description="East London renovated warehouse tube carriage live performance space.",
        ),
        Venue(
            id="ven_windmill_brixton",
            name="The Windmill (Brixton)",
            city="London",
            country="United Kingdom",
            capacity=150,
            capacity_tier=VenueCapacityTier.INTIMATE,
            genres=["Post-Punk", "Indie Rock", "Alternative"],
            sound_system="Grassroots Club PA",
            booking_email="windmillbrixton@gmail.com",
            description="The undisputed UK incubator for breakthrough guitar and indie acts.",
        ),
        # === NEW YORK CITY ===
        Venue(
            id="ven_bowery_ballroom",
            name="The Bowery Ballroom",
            city="New York City",
            country="United States",
            capacity=575,
            capacity_tier=VenueCapacityTier.CLUB,
            genres=["Indie Pop", "Rock", "Neo-Soul", "Electronic"],
            sound_system="d&b audiotechnik Soundscape",
            booking_email="booking@boweryballroom.com",
            description="NYC's premier acoustic and indie breakthrough live music ballroom.",
        ),
        Venue(
            id="ven_elsewhere",
            name="Elsewhere (Brooklyn)",
            city="New York City",
            country="United States",
            capacity=1200,
            capacity_tier=VenueCapacityTier.HALL,
            genres=["Electronic", "Indie Dance", "Techno", "Hip-Hop"],
            sound_system="Funktion-One Multi-Room Array",
            booking_email="booking@elsewherebrooklyn.com",
            description="Multi-room music and arts venue and creative community center.",
        ),
        Venue(
            id="ven_babys_all_right",
            name="Baby's All Right",
            city="New York City",
            country="United States",
            capacity=250,
            capacity_tier=VenueCapacityTier.INTIMATE,
            genres=["Bedroom Pop", "Neo-Soul", "Indie Rock", "Electronic"],
            sound_system="Custom LED Backlit Acoustic PA",
            booking_email="booking@babysallright.com",
            description="Williamsburg launchpad for emerging US debut acts.",
        ),
        # === LOS ANGELES ===
        Venue(
            id="ven_troubadour",
            name="The Troubadour (West Hollywood)",
            city="Los Angeles",
            country="United States",
            capacity=500,
            capacity_tier=VenueCapacityTier.CLUB,
            genres=["Indie Rock", "Pop", "Folk", "Alternative"],
            sound_system="L-Acoustics ARCS",
            booking_email="booking@troubadour.com",
            description="Historic Hollywood live music landmark where icons debuted.",
        ),
        Venue(
            id="ven_echoplex",
            name="The Echo & Echoplex",
            city="Los Angeles",
            country="United States",
            capacity=700,
            capacity_tier=VenueCapacityTier.CLUB,
            genres=["Indie Dance", "Hip-Hop", "Post-Punk", "Electronic"],
            sound_system="d&b audiotechnik J-Series",
            booking_email="info@theecho.com",
            description="Echo Park underground music staple and touring hotspot.",
        ),
        # === AMSTERDAM & PARIS ===
        Venue(
            id="ven_paradiso",
            name="Paradiso Amsterdam",
            city="Amsterdam",
            country="Netherlands",
            capacity=1500,
            capacity_tier=VenueCapacityTier.HALL,
            genres=["Pop", "Electronic", "Rock", "World"],
            sound_system="d&b audiotechnik KSL",
            booking_email="programma@paradiso.nl",
            description="Converted historic church and legendary European tour stop.",
        ),
        Venue(
            id="ven_rex_club",
            name="Rex Club (Paris)",
            city="Paris",
            country="France",
            capacity=800,
            capacity_tier=VenueCapacityTier.CLUB,
            genres=["French House", "Techno", "Electro"],
            sound_system="d&b audiotechnik C-Series",
            booking_email="booking@rexclub.com",
            description="The historic Paris underground temple for electronic and house music.",
        ),
        # === LAGOS & KINGSTON ===
        Venue(
            id="ven_afrika_shrine",
            name="The New Afrika Shrine",
            city="Lagos",
            country="Nigeria",
            capacity=2500,
            capacity_tier=VenueCapacityTier.ARENA,
            genres=["Afrobeat", "Afropop", "Highlife"],
            sound_system="High-Power Open-Air PA Array",
            booking_email="shrine@felakuti.com",
            description="The spiritual home of Afrobeat and live African music.",
        ),
        Venue(
            id="ven_dub_club_kin",
            name="Kingston Dub Club (Skyline Drive)",
            city="Kingston",
            country="Jamaica",
            capacity=400,
            capacity_tier=VenueCapacityTier.CLUB,
            genres=["Reggae", "Roots Dub", "Sound System"],
            sound_system="Custom Hand-Built Heavy Bass Sound System",
            booking_email="dubclub@kingston.jm",
            description="Open-air mountaintop sound system sanctuary overlooking Kingston.",
        ),
    ]

    @classmethod
    def get_venue(cls, venue_id: str) -> Optional[Venue]:
        for v in cls.VENUES:
            if v.id == venue_id:
                return v
        return None

    @classmethod
    def list_venues(
        cls, city: Optional[str] = None, tier: Optional[str] = None
    ) -> List[Venue]:
        results = cls.VENUES
        if city:
            results = [v for v in results if city.lower() in v.city.lower()]
        if tier:
            results = [v for v in results if v.capacity_tier.value == tier.lower()]
        return results
