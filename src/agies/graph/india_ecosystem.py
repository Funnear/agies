"""India Music Industry & Subcultural Knowledge Graph Engine.

Constructs the comprehensive music ecosystem of India starting from Mumbai and
branching through major domestic hubs and international diaspora corridors:

1. Mumbai Ground Zero:
   - Districts: Bandra West, Khar/Santacruz, Andheri West/Versova, Lower Parel (Todi Mills)
   - Historic Studios: YRF Studios, Island City Studios, Empire Studio, Cotton Press
   - Grassroots Clubs & Venues: antiSOCIAL Mumbai, Bonobo Bandra, G5A Warehouse, Khar Social
   - Collectives & Record Labels: Azadi Records, Gully Gang, Krunk (Bass Camp), Mass Appeal India
   - Vinyl & Community Media: The Revolver Club, Adagio, Boxout.fm
2. Goa Psytrance & Coastal Techno Circuit (Vagator, Anjuna, HillTop Goa, House of Chapora, Shiva Valley)
3. Bengaluru Indie, Synth & Drum'n'Bass Capital (Fandom Koramangala, Pebble Palace Grounds, Windmills)
4. New Delhi Hip-Hop, Jazz & Experimental Axis (Auro Kitchen, Summer House, The Piano Man, Magnetic Fields Festival)
5. Kolkata Jazz & Rock Heritage (Someplace Else, Skinny Mo's)
6. Chennai & Kochi Carnatic & Scoring Titan (A.R. Rahman's Panchathan Record Inn, Fort Kochi)
7. Inter-City Domestic Corridors (Mumbai <-> Goa, Mumbai <-> Delhi, Mumbai <-> Bengaluru) & Transnational Lineages.
"""

import logging
from typing import Any, Dict, List

from agies.graph.builder import MusicIndustryGraph
from agies.graph.schema import (
    BaseEntity,
    EntityType,
)

logger = logging.getLogger("agies.graph.india_ecosystem")


class IndiaMusicEcosystemBuilder:
    """Ingests the full Indian music ecosystem, institutions, and corridors."""

    INDIAN_CITIES_INFRASTRUCTURE: List[Dict[str, Any]] = [
        # === MUMBAI GROUND ZERO ===
        {
            "id": "city_mumbai",
            "name": "Mumbai",
            "country": "India",
            "hub_type": "National Commercial, Hip-Hop & Electronic Epicenter",
            "acoustic_signature": "Gully rap 808s (95-140 BPM), Bollywood orchestral scoring, and underground bass",
            "venues": [
                {"id": "ven_antisocial_mumbai", "name": "antiSOCIAL Mumbai (Lower Parel)", "sound": "Custom High-Power Club PA", "desc": "Subterranean warehouse venue in Todi Mills hosting cutting-edge underground techno, hip-hop, and modular live sets."},
                {"id": "ven_bonobo_mumbai", "name": "Bonobo (Bandra West)", "sound": "Acoustic Rooftop Hi-Fi", "desc": "Legendary Bandra rooftop bar that incubated Mumbai's underground electronica, funk, jazz, and selector community since 2008."},
                {"id": "ven_g5a_mumbai", "name": "G5A Warehouse (Mahalaxmi)", "sound": "Acoustically Treated Black Box Theater", "desc": "Restored mill warehouse hosting experimental sound art, jazz, neo-classical, and multidisciplinary performances."},
                {"id": "ven_khar_social", "name": "Khar Social", "sound": "Live Gig Stage PA", "desc": "Suburban music hub and live indie launchpad in Khar West."},
                {"id": "ven_ncpa_mumbai", "name": "NCPA (National Centre for the Performing Arts)", "sound": "Symphony & Classical Acoustic Hall", "desc": "Nariman Point cultural institution housing the Symphony Orchestra of India."},
            ],
            "studios": [
                {"id": "std_yrf_mumbai", "name": "YRF Studios (Andheri West)", "sound": "Dolby Atmos Premier & Large Scoring Stage", "desc": "Yash Raj Films' world-class scoring stages, SSL Duality consoles, and premier audio post-production facilities."},
                {"id": "std_islandcity_mumbai", "name": "Island City Studios (Khar)", "sound": "Custom Rupert Neve 5088 Discrete Console", "desc": "State-of-the-art live room and analog recording haven in Khar West for India's top indie and playback musicians."},
                {"id": "std_cottonpress_mumbai", "name": "Cotton Press Studio (Lower Parel)", "sound": "Vintage Tube & Analog Tape Suite", "desc": "Boutique studio famous for live acoustic sessions and indie rock tracking."},
            ],
            "labels_collectives": [
                {"id": "lbl_azadi_records", "name": "Azadi Records", "desc": "Trailblazing independent record label pioneering socio-political South Asian hip-hop (Seedhe Maut, Prabh Deep, Ahmer, Tienas)."},
                {"id": "lbl_gully_gang", "name": "Gully Gang Records", "desc": "DIVINE's hip-hop imprint documenting authentic Mumbai street cyphers and next-generation Indian rap."},
                {"id": "coll_krunk_mumbai", "name": "Krunk & Bass Camp Festival", "desc": "Sohail Arora's pioneering music agency that brought global bass music, dubstep, and drum'n'bass to India."},
                {"id": "coll_boxout_fm", "name": "Boxout.fm", "desc": "Online community radio station broadcasting eclectic underground sounds across the Indian subcontinent 24/7."},
                {"id": "store_revolver_club", "name": "The Revolver Club (Mahim)", "desc": "India's premier vinyl store, turntable dispensary, and audiophile community anchor."},
            ],
            "artists": [
                {"id": "art_divine", "name": "DIVINE", "subgenre": "hip_hop", "bpm": 135.0, "desc": "Pioneer of the Gully Rap movement from Mumbai's streets, signed to Mass Appeal India and founder of Gully Gang."},
                {"id": "art_sandunes", "name": "Sandunes (Sanaya Ardeshir)", "subgenre": "ambient_downtempo", "bpm": 115.0, "desc": "Mumbai keyboardist, composer, and electronic producer blending organic piano acoustics with modular synthesizers and UK garage rhythms."},
                {"id": "art_dualist_inquiry", "name": "Dualist Inquiry (Sahej Bakshi)", "subgenre": "indie_electronic", "bpm": 124.0, "desc": "Electronic producer and guitarist pioneer who helped shape modern Indian festival electronic culture and Boxout.fm."},
            ],
            "corridors": ["city_goa", "city_delhi", "city_bengaluru", "city_pune", "city_london"],
        },

        # === GOA COASTAL AXIS ===
        {
            "id": "city_goa",
            "name": "Goa",
            "country": "India",
            "hub_type": "Psychedelic Trance, Sunset Deep House & Coastal Rave Haven",
            "acoustic_signature": "145-150 BPM Goa Trance rolling arpeggios, psybient, and sunset melodic house",
            "venues": [
                {"id": "ven_hilltop_goa", "name": "HillTop Goa (Vagator)", "sound": "Full-Spectrum Open-Air Psychoacoustic Array", "desc": "The global spiritual mecca of Goa trance perched on Vagator's hills since the early 1980s."},
                {"id": "ven_house_of_chapora", "name": "House of Chapora", "sound": "Void Acoustics Dynamic Soundfield", "desc": "Avant-garde audiovisual club and sensory experience sanctuary on the Chapora jetty."},
                {"id": "ven_shiva_valley", "name": "Shiva Valley (Anjuna)", "sound": "Beachfront Temple Rig", "desc": "Tuesday night beach institution celebrating pure psychedelic trance and Anjuna trance culture."},
            ],
            "studios": [],
            "labels_collectives": [
                {"id": "coll_hilltop_music", "name": "HillTop Music Collective", "desc": "Global psytrance label and festival production brotherhood."},
            ],
            "artists": [
                {"id": "art_arjun_vagale", "name": "Arjun Vagale", "subgenre": "techno", "bpm": 138.0, "desc": "India's techno pioneer, Asymetrik label founder, and internationally recognized dark techno producer."},
            ],
            "corridors": ["city_mumbai", "city_bengaluru", "city_berlin", "city_telaviv"],
        },

        # === BENGALURU SYNTH & BASS CAPITAL ===
        {
            "id": "city_bengaluru",
            "name": "Bengaluru",
            "country": "India",
            "hub_type": "Indie Rock, Drum'n'Bass & Hardware Synthesis Capital",
            "acoustic_signature": "174 BPM jungle/dnb, math rock guitar math, and modular synthesis",
            "venues": [
                {"id": "ven_fandom_bengaluru", "name": "Fandom at Gilly's Redefined (Koramangala)", "sound": "High-Fidelity Live Concert Rig", "desc": "Top live band venue hosting international electronic headliners and Indian indie rock titans."},
                {"id": "ven_pebble_bengaluru", "name": "Pebble - The Jungle Lounge (Palace Grounds)", "sound": "Sub-Heavy Open-Air Sound System", "desc": "Legendary jungle-themed outdoor venue for drum & bass, dub, and underground techno."},
                {"id": "ven_windmills_bengaluru", "name": "Windmills Craftworks (Whitefield)", "sound": "Meyer Sound Audiophile Jazz Room", "desc": "Acoustically pristine microbrewery and jazz theater engineered with Meyer Sound reference monitors."},
            ],
            "studios": [],
            "labels_collectives": [
                {"id": "coll_consolidate_blr", "name": "Consolidate Collective", "desc": "Rahul Giri's trailblazing leftfield electronic label and community (Sulthan, Aerate Sound)."},
            ],
            "artists": [
                {"id": "art_raghudixit", "name": "Raghu Dixit", "subgenre": "folk_fusion", "bpm": 118.0, "desc": "Iconic Indian folk-rock virtuoso fronting The Raghu Dixit Project."},
            ],
            "corridors": ["city_mumbai", "city_chennai", "city_hyderabad", "city_london"],
        },

        # === NEW DELHI HIP-HOP & HERITAGE AXIS ===
        {
            "id": "city_delhi",
            "name": "New Delhi & NCR",
            "country": "India",
            "hub_type": "Desi Hip-Hop, Jazz Cabaret & Northern Folk Axis",
            "acoustic_signature": "Desi drill 808s (140 BPM), Punjabi trap, and brassy live jazz",
            "venues": [
                {"id": "ven_auro_delhi", "name": "Auro Kitchen & Bar (Hauz Khas)", "sound": "KV2 Audio Club Rig", "desc": "Rooftop hub in Aurobindo Market for underground techno, hip-hop cyphers, and alternative culture."},
                {"id": "ven_pianoman_delhi", "name": "The Piano Man Jazz Club (Safdarjung)", "sound": "Art Deco Acoustic Cabaret", "desc": "Beloved 365-day live jazz club fostering blues, bebop, and singer-songwriters."},
                {"id": "ven_summerhouse_delhi", "name": "Summer House Cafe (Hauz Khas)", "sound": "Multi-Level Party PA", "desc": "Famous rooftop venue where international stars and local collectives perform."},
            ],
            "studios": [],
            "labels_collectives": [
                {"id": "coll_magneticfields", "name": "Magnetic Fields Festival (Alsisar)", "desc": "World-renowned boutique festival blending desert palace heritage with cutting-edge global electronic music."},
            ],
            "artists": [
                {"id": "art_seedhe_maut", "name": "Seedhe Maut (Encore ABJ & Calm)", "subgenre": "hip_hop", "bpm": 140.0, "desc": "Revolutionary New Delhi rap duo signed to Azadi Records, redefining South Asian hip-hop flow and raw storytelling."},
                {"id": "art_prabh_deep", "name": "Prabh Deep", "subgenre": "hip_hop", "bpm": 128.0, "desc": "Critically acclaimed Tilak Nagar rapper, producer, and sonic storyteller blending Punjabi poetry with intricate electronic beats."},
            ],
            "corridors": ["city_mumbai", "city_chandigarh", "city_jaipur", "city_london"],
        },

        # === CHENNAI & KOCHI SCORING & CARNATIC TITANS ===
        {
            "id": "city_chennai",
            "name": "Chennai",
            "country": "India",
            "hub_type": "Carnatic Classical & Global Cinematic Scoring Bastion",
            "acoustic_signature": "Microtonal Carnatic scales (Ragas), Mridangam polyrhythms, and symphonic film scores",
            "venues": [
                {"id": "ven_musicacademy_chennai", "name": "The Music Academy (Mylapore)", "sound": "Historic Pure Classical Acoustic Hall", "desc": "The epicentre of the December Margazhi Season, the world's largest classical music festival."},
            ],
            "studios": [
                {"id": "std_panchathan_chennai", "name": "Panchathan Record Inn (Kodambakkam)", "sound": "A.R. Rahman's Custom Euphonix/SSL Scoring Room", "desc": "A.R. Rahman's legendary Kodambakkam studio where pioneering Indian-Western electronic fusions were born."},
            ],
            "labels_collectives": [],
            "artists": [
                {"id": "art_ar_rahman", "name": "A.R. Rahman", "subgenre": "soundtrack", "bpm": 110.0, "desc": "Academy Award & Grammy winning maestro who revolutionized Indian film scoring, synthesis, and global crossover music."},
            ],
            "corridors": ["city_bengaluru", "city_mumbai", "city_kochi", "city_london", "city_losangeles"],
        },
    ]

    def enrich_india_ecosystem(self, industry_graph: MusicIndustryGraph) -> Dict[str, Any]:
        """Ingest the complete Indian music ecosystem into the Knowledge Graph."""
        graph = industry_graph.graph
        stats = {
            "cities_added": 0,
            "venues_added": 0,
            "studios_added": 0,
            "labels_collectives_added": 0,
            "artists_added": 0,
            "india_corridors_added": 0,
        }

        for city_data in self.INDIAN_CITIES_INFRASTRUCTURE:
            cid = city_data["id"]
            # 1. Ingest City Node
            if cid not in graph:
                city_ent = BaseEntity(
                    id=cid,
                    name=city_data["name"],
                    entity_type=EntityType.TRACK,
                    country=city_data["country"],
                    description=f"{city_data['name']} is an essential Indian music hub: {city_data['hub_type']}. Acoustic signature: {city_data['acoustic_signature']}.",
                    attributes={
                        "category": "Indian Music Hub",
                        "hub_type": city_data["hub_type"],
                        "acoustic_signature": city_data["acoustic_signature"],
                    },
                )
                industry_graph.add_entity(city_ent)
                stats["cities_added"] += 1

            # 2. Ingest Venues
            for v in city_data.get("venues", []):
                vid = v["id"]
                if vid not in graph:
                    v_ent = BaseEntity(
                        id=vid,
                        name=v["name"],
                        entity_type=EntityType.STUDIO,
                        country="India",
                        description=v["desc"],
                        attributes={"city": city_data["name"], "sound_system": v.get("sound", "Club PA")},
                    )
                    industry_graph.add_entity(v_ent)
                    stats["venues_added"] += 1

                if not graph.has_edge(vid, cid):
                    graph.add_edge(vid, cid, rel_type="LOCATED_IN_CITY", weight=1.0)

            # 3. Ingest Studios
            for s in city_data.get("studios", []):
                sid = s["id"]
                if sid not in graph:
                    s_ent = BaseEntity(
                        id=sid,
                        name=s["name"],
                        entity_type=EntityType.STUDIO,
                        country="India",
                        description=s["desc"],
                        attributes={"city": city_data["name"], "console_specs": s.get("sound", "Analog Console")},
                    )
                    industry_graph.add_entity(s_ent)
                    stats["studios_added"] += 1

                if not graph.has_edge(sid, cid):
                    graph.add_edge(sid, cid, rel_type="OPERATES_IN_CITY", weight=1.0)

            # 4. Ingest Labels & Collectives
            for lc in city_data.get("labels_collectives", []):
                lcid = lc["id"]
                if lcid not in graph:
                    lc_ent = BaseEntity(
                        id=lcid,
                        name=lc["name"],
                        entity_type=EntityType.RECORD_LABEL,
                        country="India",
                        description=lc["desc"],
                        attributes={"city": city_data["name"]},
                    )
                    industry_graph.add_entity(lc_ent)
                    stats["labels_collectives_added"] += 1

                if not graph.has_edge(lcid, cid):
                    graph.add_edge(lcid, cid, rel_type="BASED_IN_CITY_HUB", weight=1.0)

            # 5. Ingest Artists
            for art in city_data.get("artists", []):
                aid = art["id"]
                if aid not in graph:
                    a_ent = BaseEntity(
                        id=aid,
                        name=art["name"],
                        entity_type=EntityType.ARTIST,
                        country="India",
                        description=art["desc"],
                        genres=[art["subgenre"]],
                        attributes={"city": city_data["name"], "bpm": art["bpm"], "classified_subgenre": art["subgenre"]},
                    )
                    industry_graph.add_entity(a_ent)
                    stats["artists_added"] += 1

                if not graph.has_edge(aid, cid):
                    graph.add_edge(aid, cid, rel_type="BASED_IN_CITY", weight=1.0)

            # 6. Inter-City Corridors
            for target_corridor in city_data.get("corridors", []):
                if target_corridor in graph and not graph.has_edge(cid, target_corridor):
                    graph.add_edge(
                        cid,
                        target_corridor,
                        rel_type="GEOGRAPHIC_CORRIDOR",
                        weight=0.92,
                        is_indian_corridor=True,
                    )
                    stats["india_corridors_added"] += 1

        logger.info(
            "India Music Ecosystem Ingested: %d cities, %d venues, %d studios, %d labels, %d artists, %d corridors.",
            stats["cities_added"],
            stats["venues_added"],
            stats["studios_added"],
            stats["labels_collectives_added"],
            stats["artists_added"],
            stats["india_corridors_added"],
        )

        return stats
