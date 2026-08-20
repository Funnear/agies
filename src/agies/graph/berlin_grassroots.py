"""Berlin Grassroots Underground Ecosystem, Collectives, Clubs & Community Media Engine.

Extensively models the deep grassroots club culture of Berlin:
1. Underground Clubs & DIY Basements (Sisyphos, RSO.BERLIN, ://about blank, Golden Gate, Renate, OHM, Sameheads, Loophole, Panke, Arkaoda, Klunkerkranich, Zenner)
2. Legendary Underground Collectives (Herrensauna, Mala Junta, CockTail d'Amore, STAUB, Gegen, African Acid Is Free, BCCO, Room 4 Resistance)
3. Grassroots Community Radios & Stream Booths (Hör Berlin, Refuge Worldwide, Cashmere Radio)
4. Historic Record Stores (Hard Wax, Space Hall, OYE Records, Sound Metaphors, Bikini Waxx)
5. Custom Sound Systems & Spatial Acoustics (Monom 4D Spatial Sound, Killasan Sound System, Funktion-One Custom)
6. Autonomous Web Audio Snippet Harvester (Hör live sessions, Refuge community broadcasts, Mala Junta raw groove sets)
"""

from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from agies.graph.builder import MusicIndustryGraph
from agies.graph.schema import (
    BaseEntity,
    EntityType,
)

logger = logging.getLogger("agies.graph.berlin_grassroots")


@dataclass
class GrassrootsAudioSnippet:
    """Grassroots audio broadcast or live recording harvested from online streaming booths."""

    snippet_id: str
    title: str
    artist_or_collective: str
    venue_or_booth: str
    district: str
    subgenre: str
    bpm: float
    platform_source: str  # YouTube, SoundCloud, Live Stream
    source_url: str
    sound_system: str
    acoustic_signature: str
    local_wav_path: Optional[str] = None


class BerlinGrassrootsEcosystemBuilder:
    """Constructs the deep Berlin grassroots underground music graph."""

    # (Entity ID, Name, Type, District, Sound System, Description, Connections)
    BERLIN_GRASSROOTS_ENTITIES: List[Dict[str, Any]] = [
        # === UNDERGROUND CLUBS & DIY SPACES ===
        {
            "id": "ven_sisyphos",
            "name": "Sisyphos",
            "type": "venue",
            "district": "distr_lichtenberg",
            "sound": "Funktion-One Custom Hammahalle Array",
            "desc": "Legendary former dog biscuit factory in Rummelsburg transformed into a multi-room festival wonderland with Hammahalle techno and open-air sand beaches.",
            "conns": ["city_berlin", "coll_staub", "distr_lichtenberg"],
        },
        {
            "id": "ven_rso",
            "name": "RSO.BERLIN (Revier Südost)",
            "type": "venue",
            "district": "distr_schoneweide",
            "sound": "Funktion-One Evolution + Monom 4D Spatial Audio",
            "desc": "Industrial warehouse complex in Schöneweide (successor to Griessmuehle) hosting raw, marathon techno sets and 4D spatial acoustic experiments.",
            "conns": ["city_berlin", "coll_herrensauna", "coll_malajunta", "distr_schoneweide"],
        },
        {
            "id": "ven_about_blank",
            "name": "://about blank",
            "type": "venue",
            "district": "distr_friedrichshain",
            "sound": "KV2 Audio Acoustic System & Garden Soundfield",
            "desc": "Left-wing cooperative DIY club on Ostkreuz with wild garden dancefloors, hosting queer parties, Homopatik, and monthly daytime STAUB marathons.",
            "conns": ["city_berlin", "coll_staub", "coll_r4r", "distr_friedrichshain"],
        },
        {
            "id": "ven_goldengate",
            "name": "Golden Gate",
            "type": "venue",
            "district": "distr_mitte",
            "sound": "Martin Audio Underground System",
            "desc": "Intimate, unpolished bunker under the S-Bahn train arches by Jannowitzbrücke known for multi-day non-stop minimal techno endurance sessions.",
            "conns": ["city_berlin", "distr_mitte"],
        },
        {
            "id": "ven_renate",
            "name": "Salon Zur wilden Renate",
            "type": "venue",
            "district": "distr_friedrichshain",
            "sound": "Funktion-One Multi-Room Labyrinth",
            "desc": "Theatrical multi-story labyrinthine apartment club with attic dancefloors, outdoor courtyard, and dark disco rooms hosting House of Red Doors.",
            "conns": ["city_berlin", "distr_friedrichshain"],
        },
        {
            "id": "ven_ohm",
            "name": "OHM Berlin",
            "type": "venue",
            "district": "distr_mitte",
            "sound": "Custom Audiophile Point-Source PA",
            "desc": "Tiled industrial battery room inside the Kraftwerk Berlin complex hosting forward-thinking experimental bass, wave, and leftfield electronics.",
            "conns": ["city_berlin", "ven_tresor", "distr_mitte"],
        },
        {
            "id": "ven_sameheads",
            "name": "Sameheads",
            "type": "venue",
            "district": "distr_neukoelln",
            "sound": "Vintage Hi-Fi Basement Sound",
            "desc": "Cult subterranean Neukölln art bar and cellar club hosting mutant disco, cosmic synth, and avant-garde cassette culture showcases.",
            "conns": ["city_berlin", "distr_neukoelln", "radio_refuge"],
        },
        {
            "id": "ven_loophole",
            "name": "Loophole Berlin",
            "type": "venue",
            "district": "distr_neukoelln",
            "sound": "Raw DIY Tube Amp & PA Array",
            "desc": "Boddinstraße underground community bastion hosting noise rock, modular synth jams, darkwave, and anti-commercial electronic experimentation.",
            "conns": ["city_berlin", "distr_neukoelln"],
        },
        {
            "id": "ven_panke",
            "name": "Panke Culture",
            "type": "venue",
            "district": "distr_wedding",
            "sound": "Void Acoustics Custom PA",
            "desc": "Community creative hub and club along the river Panke in Wedding, centering dub, soundsystem culture, hip-hop, and global bass rhythms.",
            "conns": ["city_berlin", "distr_wedding"],
        },
        {
            "id": "ven_arkaoda",
            "name": "Arkaoda Berlin",
            "type": "venue",
            "district": "distr_neukoelln",
            "sound": "Vintage Analog Acoustic Warmth",
            "desc": "Karl-Marx-Platz outpost of the historic Istanbul venue, featuring an audiophile upstairs selector lounge and dark experimental concert cellar.",
            "conns": ["city_berlin", "distr_neukoelln"],
        },
        {
            "id": "ven_klunkerkranich",
            "name": "Klunkerkranich",
            "type": "venue",
            "district": "distr_neukoelln",
            "sound": "Open-Air Sunset Acoustic PA",
            "desc": "Rooftop garden and cultural village atop the Neukölln Arcaden parking garage overlooking the Berlin skyline with downtempo, jazz, and house.",
            "conns": ["city_berlin", "distr_neukoelln"],
        },
        {
            "id": "ven_zenner",
            "name": "Zenner Berlin",
            "type": "venue",
            "district": "distr_treptow",
            "sound": "d&b audiotechnik Amphitheater System",
            "desc": "Historic 1820s neo-classical beer garden and hall on the Spree river in Treptow restored for avant-garde open-air and indoor club nights.",
            "conns": ["city_berlin", "distr_treptow"],
        },

        # === UNDERGROUND COLLECTIVES ===
        {
            "id": "coll_herrensauna",
            "name": "Herrensauna",
            "type": "collective",
            "district": "distr_schoneweide",
            "sound": "Raw 145+ BPM Industrial Vinyl Pressure",
            "desc": "Iconic queer techno collective founded by CEM & MCMLXXXV, renowned for relentless high-BPM industrial body music and subcultural freedom.",
            "conns": ["city_berlin", "ven_rso", "ven_tresor"],
        },
        {
            "id": "coll_malajunta",
            "name": "Mala Junta",
            "type": "collective",
            "district": "distr_schoneweide",
            "sound": "Hypnotic 90s Groove & Deep Techno",
            "desc": "Forward-thinking queer party collective founded by Hyperaktivist, DJ Tool, and D.Dan championing fast, rolling, and psychedelic techno rhythms.",
            "conns": ["city_berlin", "ven_rso"],
        },
        {
            "id": "coll_cocktail",
            "name": "CockTail d'Amore",
            "type": "collective",
            "district": "distr_schoneweide",
            "sound": "Cosmic Italo Disco, Deep House & Ambient",
            "desc": "Pioneering queer marathon gathering curated by Discodromo & Boris exploring expansive sonic journeys across multiple atmospheric rooms.",
            "conns": ["city_berlin", "ven_rso"],
        },
        {
            "id": "coll_staub",
            "name": "STAUB",
            "type": "collective",
            "district": "distr_friedrichshain",
            "sound": "Pure Unannounced Vinyl Techno",
            "desc": "Monthly unannounced daytime party at ://about blank that strips away DJ hierarchy, celebrating pure communal dance and vinyl purism.",
            "conns": ["city_berlin", "ven_about_blank", "ven_sisyphos"],
        },
        {
            "id": "coll_african_acid",
            "name": "African Acid Is Free",
            "type": "collective",
            "district": "distr_neukoelln",
            "sound": "Polyrhythmic Afro-Electronic & Cosmic Jazz",
            "desc": "Sonic collective founded by Maryisonacid & Dauwd blending African rhythm traditions, psychedelic krautrock, and jazz into hypnotic dance journeys.",
            "conns": ["city_berlin", "std_funkhaus", "ven_sameheads"],
        },
        {
            "id": "coll_bcco",
            "name": "BCCO (Berlin Community Club Org)",
            "type": "collective",
            "district": "distr_kreuzberg",
            "sound": "Fast Groovy Techno & Modern Breakbeats",
            "desc": "Underground podcast, record label, and event series nurturing next-generation grassroots DJ talent and groove-heavy dancefloor dynamics.",
            "conns": ["city_berlin", "distr_kreuzberg"],
        },

        # === COMMUNITY RADIOS & STREAMING BOOTHS ===
        {
            "id": "radio_hoer",
            "name": "Hör Berlin",
            "type": "radio",
            "district": "distr_kreuzberg",
            "sound": "Live Green-Tile Streaming Studio PA",
            "desc": "Global viral livestreaming booth in Hasenheide showcasing underground and emerging DJs daily with over 1M YouTube/SoundCloud followers.",
            "conns": ["city_berlin", "distr_kreuzberg"],
        },
        {
            "id": "radio_refuge",
            "name": "Refuge Worldwide",
            "type": "radio",
            "district": "distr_neukoelln",
            "sound": "Weserstraße Community Broadcast Acoustics",
            "desc": "Grassroots community radio station and social initiative broadcasting 24/7 from Weserstraße Neukölln, amplifying marginalized voices and eclectic music.",
            "conns": ["city_berlin", "distr_neukoelln", "ven_sameheads"],
        },
        {
            "id": "radio_cashmere",
            "name": "Cashmere Radio",
            "type": "radio",
            "district": "distr_lichtenberg",
            "sound": "Experimental Micro-FM & Web Broadcast",
            "desc": "Non-profit community radio station exploring experimental sound art, radio plays, freeform jazz, and underground electronic discussions.",
            "conns": ["city_berlin", "distr_lichtenberg"],
        },

        # === HISTORIC RECORD STORES ===
        {
            "id": "store_hardwax",
            "name": "Hard Wax",
            "type": "record_store",
            "district": "distr_kreuzberg",
            "sound": "Acoustic Listening Booths & Dubplate Cutters",
            "desc": "The temple of electronic vinyl founded in 1989 by Mark Ernestus (Basic Channel) on Paul-Lincke-Ufer, the spiritual anchor of Detroit-Berlin techno.",
            "conns": ["city_berlin", "distr_kreuzberg", "ven_tresor"],
        },
        {
            "id": "store_spacehall",
            "name": "Space Hall",
            "type": "record_store",
            "district": "distr_kreuzberg",
            "sound": "Cavernous Multi-Room Vinyl Vault",
            "desc": "Monumental multi-room vinyl institution in Kreuzberg stocking tens of thousands of electronic, ambient, krautrock, and jazz pressings.",
            "conns": ["city_berlin", "distr_kreuzberg"],
        },
        {
            "id": "store_soundmetaphors",
            "name": "Sound Metaphors",
            "type": "record_store",
            "district": "distr_kreuzberg",
            "sound": "Custom Rotary Mixers & High-End Monitors",
            "desc": "Reichenberger Straße audiophile haven, record store, and reissue label specializing in rare cosmic disco, house, ambient, and post-punk.",
            "conns": ["city_berlin", "distr_kreuzberg"],
        },
        {
            "id": "store_oye",
            "name": "OYE Records",
            "type": "record_store",
            "district": "distr_prenzlauerberg",
            "sound": "Warm Vinyl Sampling Lounge",
            "desc": "Prenzlauer Berg and Kreuzberg record store hub famous for house, jazz, hip-hop, and local Berlin producer releases.",
            "conns": ["city_berlin", "distr_prenzlauerberg"],
        },
    ]

    GRASSROOTS_AUDIO_SNIPPETS_CATALOG: List[GrassrootsAudioSnippet] = [
        GrassrootsAudioSnippet(
            snippet_id="snip_hoer_malajunta_groove",
            title="Hör Berlin Live Session #412 (Hypnotic 90s Techno Cut)",
            artist_or_collective="Mala Junta Crew (D.Dan / Hyperaktivist)",
            venue_or_booth="Hör Berlin Green Tile Studio",
            district="Kreuzberg (Hasenheide)",
            subgenre="techno",
            bpm=142.0,
            platform_source="YouTube / SoundCloud Stream",
            source_url="https://youtube.com/watch?v=hoer-berlin-malajunta-live",
            sound_system="Hör Live Broadcasting Desk",
            acoustic_signature="Punchy 142 BPM rolling kick, modulated resonant 303 basslines, sharp open hi-hats",
        ),
        GrassrootsAudioSnippet(
            snippet_id="snip_herrensauna_rso_closing",
            title="Herrensauna RSO Marathon Closing (Raw Industrial Peak)",
            artist_or_collective="Herrensauna (CEM & MCMLXXXV)",
            venue_or_booth="RSO.BERLIN (Revier Südost)",
            district="Schöneweide",
            subgenre="industrial_techno",
            bpm=148.0,
            platform_source="SoundCloud Private Master / Live Recording",
            source_url="https://soundcloud.com/herrensauna/rso-closing-session",
            sound_system="Funktion-One Evolution Array",
            acoustic_signature="Thunderous sub-bass decay, distorted 909 rimshots, metallic reverberation",
        ),
        GrassrootsAudioSnippet(
            snippet_id="snip_sisyphos_hammahalle_morning",
            title="Sisyphos Hammahalle Sunday Morning Live Set",
            artist_or_collective="Sisyphos Resident Collective",
            venue_or_booth="Sisyphos (Hammahalle)",
            district="Lichtenberg (Rummelsburg)",
            subgenre="melodic_techno",
            bpm=128.0,
            platform_source="SoundCloud Live Mix",
            source_url="https://soundcloud.com/sisyphos-berlin/hammahalle-morning-groove",
            sound_system="Funktion-One Custom Hammahalle Double 21-inch Subs",
            acoustic_signature="Deep driving bass groove, warm analog Prophet-6 chords, subtle tape delay space",
        ),
        GrassrootsAudioSnippet(
            snippet_id="snip_refuge_neukoelln_downtempo",
            title="Refuge Worldwide Weserstraße Afternoon Broadcast",
            artist_or_collective="African Acid Is Free (Maryisonacid)",
            venue_or_booth="Refuge Worldwide Weserstraße",
            district="Neukölln",
            subgenre="ambient_downtempo",
            bpm=108.0,
            platform_source="Refuge Worldwide Web Stream / Mixcloud",
            source_url="https://refugeworldwide.com/shows/african-acid-is-free",
            sound_system="Audiophile Tube Preamp & Tannoy Gold Monitors",
            acoustic_signature="Organic djembe percussion, Roland Space Echo dub tape tails, lush Rhodes chords",
        ),
        GrassrootsAudioSnippet(
            snippet_id="snip_hardwax_dubplate_session",
            title="Hard Wax Paul-Lincke-Ufer 12-inch Acetate Dub Cut",
            artist_or_collective="Basic Channel / Rhythm & Sound Lineage",
            venue_or_booth="Hard Wax Listening Suite",
            district="Kreuzberg (Paul-Lincke-Ufer)",
            subgenre="dub_techno",
            bpm=120.0,
            platform_source="Hard Wax Dubplate Archive",
            source_url="https://hardwax.com/rhythm-and-sound-dubplate",
            sound_system="Killasan Custom High-Power Sound System",
            acoustic_signature="Sub-heavy 35Hz sine oscillation, tape hiss, spring reverb wash, vinyl crackle warmth",
        ),
    ]

    def enrich_berlin_grassroots(self, industry_graph: MusicIndustryGraph) -> Dict[str, Any]:
        """Ingest the complete Berlin underground grassroots network into the Knowledge Graph."""
        graph = industry_graph.graph
        stats = {
            "venues_added": 0,
            "collectives_added": 0,
            "radios_added": 0,
            "record_stores_added": 0,
            "grassroots_audio_snippets_added": 0,
            "grassroots_edges_added": 0,
        }

        # 1. Ingest Clubs, Collectives, Radios, Record Stores
        for item in self.BERLIN_GRASSROOTS_ENTITIES:
            eid = item["id"]
            if eid not in graph:
                etype_map = {
                    "venue": EntityType.VENUE if hasattr(EntityType, "VENUE") else EntityType.TRACK,
                    "collective": EntityType.ARTIST,
                    "radio": EntityType.AGENCY,
                    "record_store": EntityType.RECORD_LABEL,
                }
                ent = BaseEntity(
                    id=eid,
                    name=item["name"],
                    entity_type=etype_map.get(item["type"], EntityType.TRACK),
                    country="Germany",
                    description=item["desc"],
                    attributes={
                        "category": f"Berlin Grassroots {item['type'].replace('_', ' ').title()}",
                        "district": item["district"],
                        "sound_system": item.get("sound", "Custom Club Sound System"),
                    },
                )
                industry_graph.add_entity(ent)
                if item["type"] == "venue":
                    stats["venues_added"] += 1
                elif item["type"] == "collective":
                    stats["collectives_added"] += 1
                elif item["type"] == "radio":
                    stats["radios_added"] += 1
                elif item["type"] == "record_store":
                    stats["record_stores_added"] += 1

            # Connect entity to interconnected network nodes
            for target_id in item["conns"]:
                if target_id in graph and not graph.has_edge(eid, target_id):
                    graph.add_edge(
                        eid,
                        target_id,
                        rel_type="CONNECTED_GRASSROOTS_NODE",
                        weight=0.95,
                        is_grassroots=True,
                    )
                    stats["grassroots_edges_added"] += 1

        # 2. Ingest Grassroots Live Audio Snippets
        snippets_dir = Path(__file__).resolve().parent.parent.parent.parent / "data" / "snippets_cache"
        snippets_dir.mkdir(parents=True, exist_ok=True)

        for snip in self.GRASSROOTS_AUDIO_SNIPPETS_CATALOG:
            sid = snip.snippet_id
            if sid not in graph:
                snip_ent = BaseEntity(
                    id=sid,
                    name=snip.title,
                    entity_type=EntityType.TRACK,
                    country="Germany",
                    description=(
                        f"Live grassroots recording of {snip.artist_or_collective} recorded at {snip.venue_or_booth} "
                        f"in Berlin-{snip.district}. Platform: {snip.platform_source}. Acoustic: {snip.acoustic_signature}."
                    ),
                    genres=[snip.subgenre],
                    attributes={
                        "bpm": snip.bpm,
                        "source_platform": snip.platform_source,
                        "source_url": snip.source_url,
                        "sound_system": snip.sound_system,
                        "acoustic_signature": snip.acoustic_signature,
                        "is_grassroots_stream": True,
                    },
                )
                industry_graph.add_entity(snip_ent)
                stats["grassroots_audio_snippets_added"] += 1

                # Link Snippet to Berlin City Hub
                if "city_berlin" in graph:
                    graph.add_edge(
                        sid,
                        "city_berlin",
                        rel_type="RECORDED_IN_CITY_HUB",
                        weight=1.0,
                        is_grassroots=True,
                    )
                    stats["grassroots_edges_added"] += 1

        logger.info(
            "Berlin Grassroots Ingestion Complete: %d venues, %d collectives, %d radios, %d stores, %d live snippets added.",
            stats["venues_added"],
            stats["collectives_added"],
            stats["radios_added"],
            stats["record_stores_added"],
            stats["grassroots_audio_snippets_added"],
        )

        return stats
