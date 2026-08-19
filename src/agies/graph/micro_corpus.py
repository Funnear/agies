"""Micro-Ecosystem Corpus & Pathway Engine for Emerging Musicians.

Branches the Knowledge Graph to micro-level grassroots structures:
- DIY Distribution Platforms (Bandcamp, DistroKid, TuneCore, SoundCloud)
- Curation & Discovery Gateways (COLORSxSTUDIOS, BBC Introducing, Boiler Room, NPR Tiny Desk, Cercle, Submithub)
- Stepping-Stone Showcase Festivals & A&R Hubs (Reeperbahn Festival, The Great Escape, SXSW, Eurosonic ESNS, c/o pop)
- Performance Rights & Publishing Collection Societies (GEMA, PRS for Music, ASCAP, BMI, Songtrust, SoundExchange)
- Boutique Indie Incubators & Development Imprints (Erased Tapes, Soulection, Future Classic, Ninja Tune, Kompakt)
- Emerging Artist Personas across genres and development phases
"""

import logging
from typing import List, Tuple

from agies.graph.schema import (
    Artist,
    BaseEntity,
    EntityType,
    RelationshipEdge,
    RelationshipType,
)

logger = logging.getLogger("agies.graph.micro_corpus")


class MicroEcosystemCorpusExtractor:
    """Extracts micro-level stepping-stone entities and developmental pathways for starting musicians."""

    def extract(self) -> Tuple[List[BaseEntity], List[RelationshipEdge]]:
        entities: List[BaseEntity] = []
        edges: List[RelationshipEdge] = []

        # =========================================================================
        # 1. DIY DISTRIBUTION PLATFORMS
        # =========================================================================
        platforms = [
            (
                "dist_bandcamp",
                "Bandcamp",
                "Direct-to-Fan / Highest Artist Revenue Share (80-85%)",
                "Global",
            ),
            (
                "dist_distrokid",
                "DistroKid",
                "Flat-Fee Unlimited DSP Distribution / Fast Streaming Delivery",
                "USA / Global",
            ),
            (
                "dist_tunecore",
                "TuneCore",
                "Global DSP Aggregator / Publishing Administration Add-on",
                "USA / Global",
            ),
            (
                "dist_soundcloud",
                "SoundCloud (Next Pro)",
                "Community Discovery / Monetized Streaming",
                "Germany / USA",
            ),
            (
                "dist_amuse",
                "Amuse",
                "Mobile-First Free & Pro Distribution / Direct A&R Scouting",
                "Sweden / Global",
            ),
        ]

        for pid, name, desc, reg in platforms:
            ent = BaseEntity(
                id=pid,
                name=name,
                entity_type=EntityType.PRODUCTION_HOUSE,  # Tech/Distro category
                attributes={
                    "category": "DIY Distribution Platform",
                    "description": desc,
                    "region": reg,
                },
            )
            entities.append(ent)

        # =========================================================================
        # 2. CURATION & BREAKTHROUGH DISCOVERY GATEWAYS
        # =========================================================================
        curation_gateways = [
            (
                "gate_colors",
                "COLORSxSTUDIOS",
                "Berlin-based Global Live Acoustic / Aesthetic Showcase",
                "Germany / Global",
                ["R&B", "Soul", "Hip-Hop", "Indie"],
            ),
            (
                "gate_bbc_intro",
                "BBC Introducing",
                "UK Grassroots Radio & Festival Stage Launchpad",
                "UK",
                ["Indie", "Electronic", "Rock", "Pop"],
            ),
            (
                "gate_boilerroom",
                "Boiler Room",
                "Underground Club Culture & Electronic Live Stream Pioneer",
                "UK / Global",
                ["Techno", "House", "Bass", "Industrial"],
            ),
            (
                "gate_cercle",
                "Cercle",
                "Cinematic Scenic Live Electronic Performance Platform",
                "France / Global",
                ["Melodic Techno", "Deep House", "Ambient"],
            ),
            (
                "gate_tinydesk",
                "NPR Tiny Desk Concerts",
                "Intimate Unplugged Acoustic Breakthrough Stage",
                "USA / Global",
                ["Folk", "Neo-Soul", "Jazz", "Indie"],
            ),
            (
                "gate_triplej",
                "Triple J Unearthed",
                "Australian National Youth Radio Talent Discovery",
                "Australia",
                ["Indie Rock", "Electronic", "Hip-Hop"],
            ),
            (
                "gate_submithub",
                "SubmitHub / Groover",
                "Direct-to-Curator / Playlist Pitching Platform",
                "Global",
                ["All Genres"],
            ),
        ]

        for gid, name, desc, reg, gen in curation_gateways:
            ent = BaseEntity(
                id=gid,
                name=name,
                entity_type=EntityType.AGENCY,  # Promotional Agency category
                attributes={
                    "category": "Discovery & Curation Gateway",
                    "description": desc,
                    "region": reg,
                    "target_genres": gen,
                },
            )
            entities.append(ent)

        # =========================================================================
        # 3. STEPPING-STONE SHOWCASE FESTIVALS (A&R DENSITY HUBS)
        # =========================================================================
        showcase_festivals = [
            (
                "fest_reeperbahn",
                "Reeperbahn Festival (Hamburg)",
                "Europe's Largest Club Festival & B2B Music Industry Conference",
                "Germany",
                0.95,
            ),
            (
                "fest_greatescape",
                "The Great Escape (Brighton)",
                "Premier UK Showcase for Emerging Talent / 500+ New Artists",
                "UK",
                0.96,
            ),
            (
                "fest_esns",
                "Eurosonic Noorderslag (ESNS)",
                "European Talent Exchange Programme & European Booking Gateway",
                "Netherlands",
                0.94,
            ),
            (
                "fest_sxsw",
                "SXSW Music Showcase (Austin)",
                "Global Convergence for Tech, Media, and Unsigned Artists",
                "USA",
                0.92,
            ),
            (
                "fest_copop",
                "c/o pop Festival (Cologne)",
                "German Pop & Electronic Stepping-Stone Conference",
                "Germany",
                0.88,
            ),
            (
                "fest_waves",
                "Waves Vienna",
                "Central / Eastern European Music Exchange Conference",
                "Austria",
                0.85,
            ),
            (
                "fest_sonar_plus",
                "Sónar+D (Barcelona)",
                "Electronic Music Innovation, Tech & Sound Showcase",
                "Spain",
                0.91,
            ),
        ]

        for fid, name, desc, reg, ar_density in showcase_festivals:
            ent = BaseEntity(
                id=fid,
                name=name,
                entity_type=EntityType.AGENCY,
                attributes={
                    "category": "A&R Showcase Festival",
                    "description": desc,
                    "region": reg,
                    "ar_scout_density_score": ar_density,
                },
            )
            entities.append(ent)

        # =========================================================================
        # 4. RIGHTS ORGANIZATIONS & PUBLISHING ROYALTIES
        # =========================================================================
        rights_orgs = [
            (
                "rights_gema",
                "GEMA",
                "German Performing & Mechanical Rights Society",
                "Germany",
            ),
            (
                "rights_prs",
                "PRS for Music / PPL",
                "UK Performing Rights & Phonographic Performance Licensor",
                "UK",
            ),
            (
                "rights_ascap",
                "ASCAP / BMI",
                "US Performance Rights Organizations",
                "USA",
            ),
            (
                "rights_songtrust",
                "Songtrust",
                "Global Digital Publishing Royalty Administrator",
                "Global",
            ),
            (
                "rights_soundexchange",
                "SoundExchange",
                "Digital Non-Interactive Streaming Master Royalties",
                "USA",
            ),
        ]

        for rid, name, desc, reg in rights_orgs:
            ent = BaseEntity(
                id=rid,
                name=name,
                entity_type=EntityType.AGENCY,
                attributes={
                    "category": "Rights & Royalty Organization",
                    "description": desc,
                    "region": reg,
                },
            )
            entities.append(ent)

        # =========================================================================
        # 5. EMERGING ARTIST PERSONAS (Real-world Stepping-Stone Progression)
        # =========================================================================
        emerging_artists = [
            # 1. Berlin Bedroom Techno Producer (DIY -> Reeperbahn -> Ostgut)
            (
                "art_emg_berlin_tech",
                "Klangformer (Emerging Producer)",
                "Person",
                ["Techno", "Industrial"],
                2023,
                "Germany",
                "dist_bandcamp",
                "fest_reeperbahn",
                "gate_boilerroom",
                "rights_gema",
            ),
            # 2. London Neo-Soul Singer-Songwriter (DIY -> BBC Intro -> COLORS -> Beggars)
            (
                "art_emg_london_soul",
                "Maya Thorne (Emerging Soul)",
                "Person",
                ["Neo-Soul", "R&B"],
                2022,
                "UK",
                "dist_distrokid",
                "fest_greatescape",
                "gate_colors",
                "rights_prs",
            ),
            # 3. Hamburg Post-Classical Pianist (DIY -> c/o pop -> Erased Tapes)
            (
                "art_emg_hh_classical",
                "Lukas M. (Emerging Ambient Pianist)",
                "Person",
                ["Neo-Classical", "Ambient"],
                2023,
                "Germany",
                "dist_bandcamp",
                "fest_copop",
                "gate_cercle",
                "rights_gema",
            ),
            # 4. Los Angeles Bedroom Pop Artist (DIY -> Submithub -> Tiny Desk)
            (
                "art_emg_la_bedpop",
                "Echo Bloom (Emerging Indie)",
                "Person",
                ["Bedroom Pop", "Indie Rock"],
                2023,
                "USA",
                "dist_amuse",
                "fest_sxsw",
                "gate_tinydesk",
                "rights_ascap",
            ),
            # 5. Melbourne Electronic Beats Artist (DIY -> Triple J -> Future Classic)
            (
                "art_emg_melb_beats",
                "Solar Drift (Emerging Electronic)",
                "Person",
                ["Future Bass", "Lo-Fi"],
                2022,
                "Australia",
                "dist_soundcloud",
                "gate_triplej",
                "dist_bandcamp",
                "rights_ascap",
            ),
        ]

        for (
            aid,
            name,
            atype,
            genres,
            since,
            country,
            distro,
            fest,
            gate,
            rights,
        ) in emerging_artists:
            art = Artist(
                id=aid,
                name=name,
                type=atype,
                genres=genres,
                active_since=since,
                country=country,
                attributes={"development_tier": "Emerging Grassroots Artist"},
            )
            entities.append(art)

            # Link artist to their micro-ecosystem stepping stones
            edges.append(
                RelationshipEdge(
                    source_id=aid,
                    target_id=distro,
                    rel_type=RelationshipType.DISTRIBUTED_BY,
                    weight=0.9,
                )
            )
            edges.append(
                RelationshipEdge(
                    source_id=aid,
                    target_id=fest,
                    rel_type=RelationshipType.SHOWCASED_AT,
                    weight=0.85,
                )
            )
            edges.append(
                RelationshipEdge(
                    source_id=aid,
                    target_id=gate,
                    rel_type=RelationshipType.FEATURED_ON,
                    weight=0.9,
                )
            )
            edges.append(
                RelationshipEdge(
                    source_id=aid,
                    target_id=rights,
                    rel_type=RelationshipType.COLLECTS_ROYALTIES_VIA,
                    weight=1.0,
                )
            )

        # =========================================================================
        # 6. STEPPING-STONE BRIDGES (Micro -> Macro Breakthrough Highways)
        # =========================================================================
        stepping_stone_bridges = [
            # Showcase Festivals -> Major Booking & Management Discovery
            (
                "fest_reeperbahn",
                "ag_wasserman",
                RelationshipType.A_AND_R_PIPELINE,
                0.92,
            ),
            ("fest_reeperbahn", "lbl_kompakt", RelationshipType.A_AND_R_PIPELINE, 0.88),
            ("fest_greatescape", "ag_wme", RelationshipType.A_AND_R_PIPELINE, 0.95),
            ("fest_greatescape", "lbl_xl_rec", RelationshipType.A_AND_R_PIPELINE, 0.90),
            ("fest_esns", "ag_caa", RelationshipType.A_AND_R_PIPELINE, 0.91),
            ("fest_sxsw", "lbl_interscope", RelationshipType.A_AND_R_PIPELINE, 0.90),
            ("fest_copop", "lbl_erasedtapes", RelationshipType.A_AND_R_PIPELINE, 0.85),
            # Curation Gateways -> Record Label Breakthroughs
            ("gate_colors", "lbl_because", RelationshipType.A_AND_R_PIPELINE, 0.92),
            ("gate_colors", "lbl_columbia", RelationshipType.A_AND_R_PIPELINE, 0.88),
            ("gate_boilerroom", "lbl_ostgut", RelationshipType.A_AND_R_PIPELINE, 0.95),
            ("gate_boilerroom", "lbl_tresor", RelationshipType.A_AND_R_PIPELINE, 0.92),
            ("gate_cercle", "lbl_armada", RelationshipType.A_AND_R_PIPELINE, 0.90),
            (
                "gate_bbc_intro",
                "lbl_parlophone",
                RelationshipType.A_AND_R_PIPELINE,
                0.94,
            ),
            ("gate_bbc_intro", "fest_greatescape", RelationshipType.SHOWCASED_AT, 0.98),
            (
                "gate_triplej",
                "lbl_futureclassic",
                RelationshipType.A_AND_R_PIPELINE,
                0.95,
            ),
            # DIY Distribution -> Indie Label Escalation
            ("dist_bandcamp", "lbl_ghostly", RelationshipType.A_AND_R_PIPELINE, 0.88),
            ("dist_bandcamp", "lbl_warp", RelationshipType.A_AND_R_PIPELINE, 0.85),
            (
                "dist_soundcloud",
                "lbl_mad_decent",
                RelationshipType.A_AND_R_PIPELINE,
                0.82,
            ),
            ("dist_amuse", "lbl_republic", RelationshipType.A_AND_R_PIPELINE, 0.80),
        ]

        for s_id, t_id, r_type, w in stepping_stone_bridges:
            edges.append(
                RelationshipEdge(
                    source_id=s_id,
                    target_id=t_id,
                    rel_type=r_type,
                    weight=w,
                    metadata={"bridge_type": "grassroots_to_macro_pipeline"},
                )
            )

        return entities, edges
