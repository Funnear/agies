"""Synthetic Industry Ecosystem Extractor.

Generates a realistic, highly connected music industry ecosystem featuring:
- Major Label Groups (Universal Music, Sony Music, Warner Music) & Independent Labels
- Prominent Talent & Management Agencies (WME, CAA, Roc Nation, Red Light)
- World-Class Studios (Abbey Road, Electric Lady, Sunset Sound, Metropolis)
- Influential Producers & Sound Engineers
- Artists with complex relationships (Label migrations, agency representations, studio reliance, collaborations)
"""

import random
from typing import List, Tuple
from agies.graph.extractors.base_extractor import BaseGraphExtractor
from agies.graph.schema import (
    Agency,
    Artist,
    BaseEntity,
    Producer,
    ProductionHouse,
    RecordLabel,
    RelationshipEdge,
    RelationshipType,
    Studio,
)


class SyntheticIndustryExtractor(BaseGraphExtractor):
    """Generates realistic music industry graph datasets for testing and pattern analytics."""

    def __init__(self, seed: int = 42):
        super().__init__(name="synthetic_ecosystem")
        self.seed = seed

    def extract(
        self, query: str = "", limit: int = 50
    ) -> Tuple[List[BaseEntity], List[RelationshipEdge]]:
        """Generate a realistic interconnected music industry ecosystem."""
        random.seed(self.seed)
        entities: List[BaseEntity] = []
        edges: List[RelationshipEdge] = []

        # 1. Major & Indie Labels
        labels_data = [
            (
                "lbl_interscope",
                "Interscope Geffen A&M",
                True,
                "Universal Music Group",
                ["Pop", "Hip-Hop", "Rock"],
            ),
            (
                "lbl_republic",
                "Republic Records",
                True,
                "Universal Music Group",
                ["Pop", "R&B", "Hip-Hop"],
            ),
            (
                "lbl_columbia",
                "Columbia Records",
                True,
                "Sony Music Entertainment",
                ["Pop", "Rock", "Alternative"],
            ),
            (
                "lbl_rca",
                "RCA Records",
                True,
                "Sony Music Entertainment",
                ["R&B", "Pop", "Electronic"],
            ),
            (
                "lbl_atlantic",
                "Atlantic Records",
                True,
                "Warner Music Group",
                ["Hip-Hop", "Pop", "Rock"],
            ),
            (
                "lbl_warp",
                "Warp Records",
                False,
                None,
                ["Electronic", "IDM", "Experimental"],
            ),
            (
                "lbl_ninja_tune",
                "Ninja Tune",
                False,
                None,
                ["Electronic", "Trip-Hop", "Downtempo"],
            ),
            (
                "lbl_4ad",
                "4AD",
                False,
                "Beggars Group",
                ["Indie Rock", "Dream Pop", "Post-Punk"],
            ),
            ("lbl_sub_pop", "Sub Pop Records", False, None, ["Grunge", "Indie Rock"]),
            (
                "lbl_def_jam",
                "Def Jam Recordings",
                True,
                "Universal Music Group",
                ["Hip-Hop", "Trap"],
            ),
        ]

        labels = []
        for lid, name, is_major, parent, genres in labels_data:
            lbl = RecordLabel(
                id=lid,
                name=name,
                is_major=is_major,
                parent_company=parent,
                genres=genres,
                attributes={"market_tier": "Tier 1" if is_major else "Independent"},
            )
            entities.append(lbl)
            labels.append(lbl)

        # 2. Production Houses
        prod_houses_data = [
            ("ph_mxm", "MXM Music Productions", ["Pop", "Dance"], "Stockholm, Sweden"),
            ("ph_jack", "Bleachers Sound Labs", ["Indie Pop", "Rock"], "New York, USA"),
            (
                "ph_shangrila",
                "Shangri-La Creative",
                ["Rock", "Hip-Hop", "Folk"],
                "Malibu, USA",
            ),
            (
                "ph_hybe",
                "HYBE Creative Studios",
                ["K-Pop", "Dance-Pop"],
                "Seoul, South Korea",
            ),
        ]

        prod_houses = []
        for pid, name, specs, city in prod_houses_data:
            ph = ProductionHouse(
                id=pid,
                name=name,
                specialties=specs,
                attributes={"city": city},
            )
            entities.append(ph)
            prod_houses.append(ph)

        # 3. Agencies (Management & Booking)
        agencies_data = [
            ("ag_wme", "WME (William Morris Endeavor)", "Booking", "Global"),
            ("ag_caa", "CAA (Creative Artists Agency)", "Booking", "Global"),
            ("ag_uta", "UTA (United Talent Agency)", "Booking", "Global"),
            ("ag_rocnation", "Roc Nation Management", "Management", "USA / UK"),
            ("ag_redlight", "Red Light Management", "Management", "USA"),
            ("ag_primary", "Primary Talent International", "Booking", "Europe"),
        ]

        agencies = []
        for aid, name, atype, reg in agencies_data:
            ag = Agency(
                id=aid,
                name=name,
                agency_type=atype,
                attributes={"region": reg},
            )
            entities.append(ag)
            agencies.append(ag)

        # 4. Recording Studios
        studios_data = [
            ("std_abbey", "Abbey Road Studios", "London", "UK", "Legendary / Tier A"),
            (
                "std_electric",
                "Electric Lady Studios",
                "New York",
                "USA",
                "Legendary / Tier A",
            ),
            ("std_sunset", "Sunset Sound Recorders", "Los Angeles", "USA", "Tier A"),
            ("std_conway", "Conway Recording Studios", "Los Angeles", "USA", "Tier A"),
            ("std_metropolis", "Metropolis Studios", "London", "UK", "Tier A"),
            ("std_rak", "RAK Studios", "London", "UK", "Tier B"),
        ]

        studios = []
        for sid, name, city, country, tier in studios_data:
            st = Studio(
                id=sid,
                name=name,
                city=city,
                country=country,
                equipment_tier=tier,
            )
            entities.append(st)
            studios.append(st)

        # 5. Producers
        producers_data = [
            (
                "prd_max",
                "Max Martin",
                "Executive Producer",
                ["Pop", "Dance"],
                ["ph_mxm"],
            ),
            (
                "prd_jack",
                "Jack Antonoff",
                "Producer / Instrumentalist",
                ["Indie Pop", "Alternative"],
                ["ph_jack"],
            ),
            (
                "prd_rick",
                "Rick Rubin",
                "Executive Producer / Sonic Architect",
                ["Rock", "Hip-Hop"],
                ["ph_shangrila"],
            ),
            (
                "prd_finneas",
                "Finneas O'Connell",
                "Producer / Songwriter",
                ["Pop", "Minimalist"],
                [],
            ),
            (
                "prd_brian",
                "Brian Eno",
                "Ambient / Avant-Garde Producer",
                ["Ambient", "Electronic"],
                [],
            ),
            (
                "prd_metro",
                "Metro Boomin",
                "Trap / Hip-Hop Producer",
                ["Hip-Hop", "Trap"],
                [],
            ),
        ]

        producers = []
        for pid, name, role, pgenres, linked_ph in producers_data:
            p = Producer(
                id=pid,
                name=name,
                role=role,
                genres=pgenres,
            )
            entities.append(p)
            producers.append(p)
            for ph_id in linked_ph:
                edges.append(
                    RelationshipEdge(
                        source_id=pid,
                        target_id=ph_id,
                        rel_type=(
                            RelationshipType.AFFILIATED_WITH
                            if hasattr(RelationshipType, "AFFILIATED_WITH")
                            else RelationshipType.REPRESENTED_BY
                        ),
                        weight=1.0,
                    )
                )

        # 6. Artists with intentional behavioural patterns
        artists_data = [
            # Pop Superstars (High Major Label loyalty, top agencies, elite producer reliance)
            (
                "art_taylor",
                "Taylor Swift",
                "Person",
                ["Pop", "Country", "Indie Folk"],
                2004,
                "USA",
                "lbl_republic",
                "ag_wme",
                "prd_jack",
                "std_electric",
            ),
            (
                "art_billie",
                "Billie Eilish",
                "Person",
                ["Pop", "Alternative"],
                2015,
                "USA",
                "lbl_interscope",
                "ag_wme",
                "prd_finneas",
                "std_sunset",
            ),
            (
                "art_dua",
                "Dua Lipa",
                "Person",
                ["Pop", "Disco"],
                2015,
                "UK",
                "lbl_atlantic",
                "ag_caa",
                "prd_max",
                "std_rak",
            ),
            (
                "art_weeknd",
                "The Weeknd",
                "Person",
                ["R&B", "Pop", "Synthwave"],
                2010,
                "Canada",
                "lbl_republic",
                "ag_caa",
                "prd_max",
                "std_conway",
            ),
            # Hip Hop & Rap (Cross-collaborations, Roc Nation, Metro Boomin)
            (
                "art_drake",
                "Drake",
                "Person",
                ["Hip-Hop", "R&B"],
                2006,
                "Canada",
                "lbl_republic",
                "ag_wme",
                "prd_metro",
                "std_sunset",
            ),
            (
                "art_kendrick",
                "Kendrick Lamar",
                "Person",
                ["Hip-Hop", "Jazz Rap"],
                2004,
                "USA",
                "lbl_interscope",
                "ag_wme",
                "prd_rick",
                "std_conway",
            ),
            (
                "art_future",
                "Future",
                "Person",
                ["Hip-Hop", "Trap"],
                2010,
                "USA",
                "lbl_rca",
                "ag_uta",
                "prd_metro",
                "std_conway",
            ),
            (
                "art_21savage",
                "21 Savage",
                "Person",
                ["Hip-Hop", "Trap"],
                2014,
                "USA",
                "lbl_rca",
                "ag_uta",
                "prd_metro",
                "std_conway",
            ),
            # Electronic & Experimental (Indie labels: Warp / Ninja Tune, studio reliance on London studios, Brian Eno)
            (
                "art_aphex",
                "Aphex Twin",
                "Person",
                ["Electronic", "IDM", "Ambient"],
                1985,
                "UK",
                "lbl_warp",
                "ag_primary",
                "prd_brian",
                "std_metropolis",
            ),
            (
                "art_bicep",
                "BICEP",
                "Group",
                ["Electronic", "Breakbeat"],
                2009,
                "UK",
                "lbl_ninja_tune",
                "ag_primary",
                None,
                "std_rak",
            ),
            (
                "art_bonobo",
                "Bonobo",
                "Person",
                ["Electronic", "Downtempo"],
                1999,
                "UK",
                "lbl_ninja_tune",
                "ag_redlight",
                None,
                "std_abbey",
            ),
            (
                "art_fourtet",
                "Four Tet",
                "Person",
                ["Electronic", "Folktronica"],
                1997,
                "UK",
                "lbl_ninja_tune",
                "ag_primary",
                None,
                "std_abbey",
            ),
            (
                "art_flyinglotus",
                "Flying Lotus",
                "Person",
                ["Electronic", "Experimental Hip Hop"],
                2005,
                "USA",
                "lbl_warp",
                "ag_wme",
                None,
                "std_electric",
            ),
            # Rock & Indie (Studio loyalty on Abbey Road / Electric Lady, Rick Rubin / Jack Antonoff)
            (
                "art_radiohead",
                "Radiohead",
                "Group",
                ["Art Rock", "Alternative Rock"],
                1985,
                "UK",
                "lbl_4ad",
                "ag_wme",
                "prd_brian",
                "std_abbey",
            ),
            (
                "art_strokes",
                "The Strokes",
                "Group",
                ["Indie Rock", "Post-Punk"],
                1998,
                "USA",
                "lbl_rca",
                "ag_caa",
                "prd_rick",
                "std_electric",
            ),
            (
                "art_arctic",
                "Arctic Monkeys",
                "Group",
                ["Indie Rock", "Garage Rock"],
                2002,
                "UK",
                "lbl_4ad",
                "ag_wme",
                None,
                "std_abbey",
            ),
            (
                "art_phoebe",
                "Phoebe Bridgers",
                "Person",
                ["Indie Rock", "Folk"],
                2014,
                "USA",
                "lbl_4ad",
                "ag_redlight",
                "prd_jack",
                "std_electric",
            ),
            (
                "art_clairo",
                "Clairo",
                "Person",
                ["Bedroom Pop", "Indie Pop"],
                2017,
                "USA",
                "lbl_republic",
                "ag_wme",
                "prd_jack",
                "std_electric",
            ),
        ]

        artists = []
        for (
            aid,
            name,
            atype,
            genres,
            since,
            country,
            cur_lbl,
            cur_ag,
            pref_prd,
            pref_std,
        ) in artists_data:
            artist = Artist(
                id=aid,
                name=name,
                type=atype,
                genres=genres,
                active_since=since,
                country=country,
            )
            entities.append(artist)
            artists.append(artist)

            # Edge 1: Current Record Label contract
            edges.append(
                RelationshipEdge(
                    source_id=aid,
                    target_id=cur_lbl,
                    rel_type=RelationshipType.SIGNED_TO,
                    start_year=since,
                    weight=1.0,
                    is_current=True,
                )
            )

            # Edge 2: Agency representation
            edges.append(
                RelationshipEdge(
                    source_id=aid,
                    target_id=cur_ag,
                    rel_type=RelationshipType.REPRESENTED_BY,
                    weight=1.0,
                    is_current=True,
                )
            )

            # Edge 3: Preferred Studio
            if pref_std:
                edges.append(
                    RelationshipEdge(
                        source_id=aid,
                        target_id=pref_std,
                        rel_type=RelationshipType.RECORDED_AT,
                        weight=0.85,
                    )
                )

            # Edge 4: Preferred Producer
            if pref_prd:
                edges.append(
                    RelationshipEdge(
                        source_id=aid,
                        target_id=pref_prd,
                        rel_type=RelationshipType.PRODUCED_BY,
                        weight=0.9,
                    )
                )

        # 7. Add Historical Label Migrations (Simulating artist churn / label hopping behaviour)
        label_migrations = [
            # Taylor Swift migrated from Big Machine (simulated indie) to Republic
            ("art_taylor", "lbl_sub_pop", 2006, 2018, "Historical First Deal"),
            # Drake migrated / joint venture from Def Jam to Republic
            ("art_drake", "lbl_def_jam", 2009, 2018, "Past Contract"),
            # Kendrick Lamar migrated from Top Dawg / Interscope to pgLang
            ("art_kendrick", "lbl_def_jam", 2004, 2011, "Early Mixtapes"),
            # Clairo moved from Fader Label to Republic
            ("art_clairo", "lbl_4ad", 2018, 2021, "Early Releases"),
        ]

        for aid, past_lbl, s_yr, e_yr, note in label_migrations:
            edges.append(
                RelationshipEdge(
                    source_id=aid,
                    target_id=past_lbl,
                    rel_type=RelationshipType.SIGNED_TO,
                    start_year=s_yr,
                    end_year=e_yr,
                    weight=0.6,
                    is_current=False,
                    metadata={"status": "expired", "note": note},
                )
            )

        # 8. Add High-Profile Collaborations (Artist <-> Artist edges)
        collaborations = [
            (
                "art_drake",
                "art_future",
                2015,
                0.95,
            ),  # What a Time to Be Alive album collab
            ("art_drake", "art_21savage", 2022, 0.95),  # Her Loss album collab
            ("art_future", "art_21savage", 2018, 0.75),
            ("art_taylor", "art_phoebe", 2021, 0.70),  # Nothing New feature
            ("art_taylor", "art_bonobo", 2022, 0.40),  # Remix
            ("art_kendrick", "art_drake", 2012, 0.60),  # Poetic Justice
            ("art_weeknd", "art_future", 2016, 0.80),  # Low Life
            ("art_dua", "art_weeknd", 2020, 0.65),  # Remixes
            ("art_fourtet", "art_bicep", 2021, 0.85),  # Electronic club collab
            ("art_fourtet", "art_aphex", 2019, 0.70),  # B2B DJ sets
            ("art_flyinglotus", "art_kendrick", 2014, 0.90),  # Never Catch Me
            ("art_phoebe", "art_clairo", 2020, 0.80),  # Indie pop circle
            ("art_radiohead", "art_fourtet", 2003, 0.75),  # Remixes
        ]

        for a1, a2, yr, w in collaborations:
            edges.append(
                RelationshipEdge(
                    source_id=a1,
                    target_id=a2,
                    rel_type=RelationshipType.COLLABORATED_WITH,
                    start_year=yr,
                    weight=w,
                    metadata={"collab_type": "track_feature_or_album"},
                )
            )

        return entities, edges
