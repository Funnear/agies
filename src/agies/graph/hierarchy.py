"""Hierarchical Geo-Spatial & Musical Taxonomy Branching Engine.

Constructs multi-level nested hierarchies:
1. Geo-Spatial Hierarchy:
   Country -> State/Region -> City/Hub -> Creative District / Local Scene
2. Musical Taxonomy Hierarchy:
   Root Genre -> Subgenre -> Micro-Genre / Scene Sound
3. Scene-Origin Bridges:
   Subgenre -[ORIGINATED_IN_SCENE]-> City/District
   Artist / Studio / Label -[BASED_IN_CITY]-> City
"""

import logging
from typing import List, Set, Tuple

from agies.graph.schema import (
    BaseEntity,
    EntityType,
    RelationshipEdge,
)

logger = logging.getLogger("agies.graph.hierarchy")


class GeoTaxonomyHierarchyBuilder:
    """Builds multi-tier Country -> State -> City -> District -> Genre hierarchical graph networks."""

    def build_hierarchy(self) -> Tuple[List[BaseEntity], List[RelationshipEdge]]:
        entities: List[BaseEntity] = []
        edges: List[RelationshipEdge] = []
        seen_entities: Set[str] = set()

        def add_ent(e: BaseEntity):
            if e.id not in seen_entities:
                entities.append(e)
                seen_entities.add(e.id)

        # =========================================================================
        # 1. COUNTRIES & STATES/REGIONS & CITIES & DISTRICTS
        # =========================================================================
        geo_tree = [
            # GERMANY
            {
                "country": ("geo_de", "Germany", "Europe"),
                "states": [
                    {
                        "state": ("state_de_be", "Berlin (Federal State)", "Germany"),
                        "cities": [
                            {
                                "city": (
                                    "city_berlin",
                                    "Berlin",
                                    "state_de_be",
                                    "Germany",
                                ),
                                "districts": [
                                    (
                                        "distr_fhain_xberg",
                                        "Friedrichshain-Kreuzberg (Club/Techno District)",
                                        "city_berlin",
                                    ),
                                    (
                                        "distr_mitte",
                                        "Berlin-Mitte (Historic & Avant-Garde District)",
                                        "city_berlin",
                                    ),
                                    (
                                        "distr_treptow",
                                        "Treptow-Köpenick (Funkhaus Complex)",
                                        "city_berlin",
                                    ),
                                ],
                            }
                        ],
                    },
                    {
                        "state": (
                            "state_de_nrw",
                            "North Rhine-Westphalia (NRW)",
                            "Germany",
                        ),
                        "cities": [
                            {
                                "city": (
                                    "city_cologne",
                                    "Cologne (Köln)",
                                    "state_de_nrw",
                                    "Germany",
                                ),
                                "districts": [
                                    (
                                        "distr_belgisches",
                                        "Belgisches Viertel (Indie/Pop Scene)",
                                        "city_cologne",
                                    ),
                                    (
                                        "distr_ehrenfeld",
                                        "Ehrenfeld (Electronic & Club Scene)",
                                        "city_cologne",
                                    ),
                                ],
                            },
                            {
                                "city": (
                                    "city_dusseldorf",
                                    "Düsseldorf",
                                    "state_de_nrw",
                                    "Germany",
                                ),
                                "districts": [
                                    (
                                        "distr_duss_altstadt",
                                        "Altstadt / Kling Klang Zone",
                                        "city_dusseldorf",
                                    )
                                ],
                            },
                        ],
                    },
                    {
                        "state": ("state_de_hh", "Hamburg (City-State)", "Germany"),
                        "cities": [
                            {
                                "city": (
                                    "city_hamburg",
                                    "Hamburg",
                                    "state_de_hh",
                                    "Germany",
                                ),
                                "districts": [
                                    (
                                        "distr_stpauli",
                                        "St. Pauli / Reeperbahn (Showcase & Club Quarter)",
                                        "city_hamburg",
                                    ),
                                    (
                                        "distr_schanze",
                                        "Sternschanze (Indie/Vinyl Hub)",
                                        "city_hamburg",
                                    ),
                                ],
                            }
                        ],
                    },
                    {
                        "state": ("state_de_by", "Bavaria (Bayern)", "Germany"),
                        "cities": [
                            {
                                "city": (
                                    "city_munich",
                                    "Munich (München)",
                                    "state_de_by",
                                    "Germany",
                                ),
                                "districts": [
                                    (
                                        "distr_glockenbach",
                                        "Glockenbachviertel (Disco & Club Hub)",
                                        "city_munich",
                                    )
                                ],
                            }
                        ],
                    },
                    {
                        "state": ("state_de_he", "Hesse (Hessen)", "Germany"),
                        "cities": [
                            {
                                "city": (
                                    "city_frankfurt",
                                    "Frankfurt am Main",
                                    "state_de_he",
                                    "Germany",
                                ),
                                "districts": [
                                    (
                                        "distr_sachsenhausen",
                                        "Sachsenhausen / Trance Sound Hub",
                                        "city_frankfurt",
                                    )
                                ],
                            }
                        ],
                    },
                ],
            },
            # UNITED KINGDOM
            {
                "country": ("geo_uk", "United Kingdom", "Europe"),
                "states": [
                    {
                        "state": ("state_uk_england", "England", "United Kingdom"),
                        "cities": [
                            {
                                "city": (
                                    "city_london",
                                    "London",
                                    "state_uk_england",
                                    "United Kingdom",
                                ),
                                "districts": [
                                    (
                                        "distr_soho_london",
                                        "Soho & West End (Studio Row)",
                                        "city_london",
                                    ),
                                    (
                                        "distr_hackney",
                                        "Hackney & East London (Bass & Electronic Scene)",
                                        "city_london",
                                    ),
                                    (
                                        "distr_camden",
                                        "Camden Town (Rock & Post-Punk Scene)",
                                        "city_london",
                                    ),
                                ],
                            },
                            {
                                "city": (
                                    "city_manchester",
                                    "Manchester",
                                    "state_uk_england",
                                    "United Kingdom",
                                ),
                                "districts": [
                                    (
                                        "distr_nq_mcr",
                                        "Northern Quarter (Indie & Factory Records)",
                                        "city_manchester",
                                    )
                                ],
                            },
                            {
                                "city": (
                                    "city_bristol",
                                    "Bristol",
                                    "state_uk_england",
                                    "United Kingdom",
                                ),
                                "districts": [
                                    (
                                        "distr_stpauls_bristol",
                                        "St. Pauls (Trip-Hop & Dub System Sound)",
                                        "city_bristol",
                                    )
                                ],
                            },
                        ],
                    },
                    {
                        "state": ("state_uk_scotland", "Scotland", "United Kingdom"),
                        "cities": [
                            {
                                "city": (
                                    "city_glasgow",
                                    "Glasgow",
                                    "state_uk_scotland",
                                    "United Kingdom",
                                ),
                                "districts": [
                                    (
                                        "distr_westend_glasgow",
                                        "West End (Post-Rock & Indie Hub)",
                                        "city_glasgow",
                                    )
                                ],
                            }
                        ],
                    },
                ],
            },
            # UNITED STATES
            {
                "country": ("geo_us", "United States", "North America"),
                "states": [
                    {
                        "state": ("state_us_ca", "California", "United States"),
                        "cities": [
                            {
                                "city": (
                                    "city_la",
                                    "Los Angeles",
                                    "state_us_ca",
                                    "United States",
                                ),
                                "districts": [
                                    (
                                        "distr_hollywood",
                                        "Hollywood & Sunset Blvd (Historic Recording Enclave)",
                                        "city_la",
                                    ),
                                    (
                                        "distr_silverlake",
                                        "Silver Lake & Echo Park (Indie Pop/Rock Scene)",
                                        "city_la",
                                    ),
                                    (
                                        "distr_compton",
                                        "Compton (West Coast Hip-Hop Ground Zero)",
                                        "city_la",
                                    ),
                                ],
                            }
                        ],
                    },
                    {
                        "state": ("state_us_ny", "New York State", "United States"),
                        "cities": [
                            {
                                "city": (
                                    "city_nyc",
                                    "New York City",
                                    "state_us_ny",
                                    "United States",
                                ),
                                "districts": [
                                    (
                                        "distr_greenwich",
                                        "Greenwich Village (Folk/Rock & Electric Lady)",
                                        "city_nyc",
                                    ),
                                    (
                                        "distr_williamsburg",
                                        "Williamsburg & Bushwick (Indie/Techno Scene)",
                                        "city_nyc",
                                    ),
                                    (
                                        "distr_bronx",
                                        "The Bronx (Birthplace of Hip-Hop)",
                                        "city_nyc",
                                    ),
                                ],
                            }
                        ],
                    },
                    {
                        "state": ("state_us_tn", "Tennessee", "United States"),
                        "cities": [
                            {
                                "city": (
                                    "city_nashville",
                                    "Nashville",
                                    "state_us_tn",
                                    "United States",
                                ),
                                "districts": [
                                    (
                                        "distr_musicrow",
                                        "Music Row (Country & Acoustic Publishing)",
                                        "city_nashville",
                                    )
                                ],
                            }
                        ],
                    },
                    {
                        "state": ("state_us_ga", "Georgia", "United States"),
                        "cities": [
                            {
                                "city": (
                                    "city_atlanta",
                                    "Atlanta",
                                    "state_us_ga",
                                    "United States",
                                ),
                                "districts": [
                                    (
                                        "distr_buckhead_atl",
                                        "Buckhead & Zone 6 (Trap Capital)",
                                        "city_atlanta",
                                    )
                                ],
                            }
                        ],
                    },
                    {
                        "state": ("state_us_il", "Illinois", "United States"),
                        "cities": [
                            {
                                "city": (
                                    "city_chicago",
                                    "Chicago",
                                    "state_us_il",
                                    "United States",
                                ),
                                "districts": [
                                    (
                                        "distr_southside_chi",
                                        "South Side (House Music & Chicago Blues)",
                                        "city_chicago",
                                    )
                                ],
                            }
                        ],
                    },
                    {
                        "state": ("state_us_wa", "Washington State", "United States"),
                        "cities": [
                            {
                                "city": (
                                    "city_seattle",
                                    "Seattle",
                                    "state_us_wa",
                                    "United States",
                                ),
                                "districts": [
                                    (
                                        "distr_caphill_sea",
                                        "Capitol Hill (Grunge & Sub Pop Records)",
                                        "city_seattle",
                                    )
                                ],
                            }
                        ],
                    },
                    {
                        "state": ("state_us_mi", "Michigan", "United States"),
                        "cities": [
                            {
                                "city": (
                                    "city_detroit",
                                    "Detroit",
                                    "state_us_mi",
                                    "United States",
                                ),
                                "districts": [
                                    (
                                        "distr_detroit_techno",
                                        "Detroit Techno & Motown Corridor",
                                        "city_detroit",
                                    )
                                ],
                            }
                        ],
                    },
                ],
            },
            # FRANCE
            {
                "country": ("geo_fr", "France", "Europe"),
                "states": [
                    {
                        "state": ("state_fr_idf", "Île-de-France", "France"),
                        "cities": [
                            {
                                "city": (
                                    "city_paris",
                                    "Paris",
                                    "state_fr_idf",
                                    "France",
                                ),
                                "districts": [
                                    (
                                        "distr_pigalle",
                                        "Pigalle & Montmartre (French Touch / Motorbass)",
                                        "city_paris",
                                    ),
                                    (
                                        "distr_oberkampf",
                                        "Oberkampf & Bastille (Indie Dance & Nu-Disco)",
                                        "city_paris",
                                    ),
                                ],
                            }
                        ],
                    }
                ],
            },
            # SWEDEN
            {
                "country": ("geo_se", "Sweden", "Europe"),
                "states": [
                    {
                        "state": ("state_se_sthlm", "Stockholm County", "Sweden"),
                        "cities": [
                            {
                                "city": (
                                    "city_stockholm",
                                    "Stockholm",
                                    "state_se_sthlm",
                                    "Sweden",
                                ),
                                "districts": [
                                    (
                                        "distr_sodermalm",
                                        "Södermalm (Pop Hitmakers & Indie Studios)",
                                        "city_stockholm",
                                    ),
                                    (
                                        "distr_ostermalm",
                                        "Östermalm (Cheiron / MXM Studio District)",
                                        "city_stockholm",
                                    ),
                                ],
                            }
                        ],
                    }
                ],
            },
            # JAPAN
            {
                "country": ("geo_jp", "Japan", "Asia"),
                "states": [
                    {
                        "state": ("state_jp_tokyo", "Tokyo Prefecture", "Japan"),
                        "cities": [
                            {
                                "city": (
                                    "city_tokyo",
                                    "Tokyo",
                                    "state_jp_tokyo",
                                    "Japan",
                                ),
                                "districts": [
                                    (
                                        "distr_shibuya",
                                        "Shibuya (Shibuya-kei & J-Pop Scene)",
                                        "city_tokyo",
                                    ),
                                    (
                                        "distr_shinjuku",
                                        "Shinjuku (Electronic Scoring & Sony Studios)",
                                        "city_tokyo",
                                    ),
                                    (
                                        "distr_shimokita",
                                        "Shimokitazawa (Indie Rock & Vinyl Quarter)",
                                        "city_tokyo",
                                    ),
                                ],
                            }
                        ],
                    }
                ],
            },
            # SOUTH KOREA
            {
                "country": ("geo_kr", "South Korea", "Asia"),
                "states": [
                    {
                        "state": (
                            "state_kr_seoul",
                            "Seoul Capital Area",
                            "South Korea",
                        ),
                        "cities": [
                            {
                                "city": (
                                    "city_seoul",
                                    "Seoul",
                                    "state_kr_seoul",
                                    "South Korea",
                                ),
                                "districts": [
                                    (
                                        "distr_gangnam",
                                        "Gangnam (K-Pop Entertainment Agency Strip)",
                                        "city_seoul",
                                    ),
                                    (
                                        "distr_hongdae",
                                        "Hongdae (Indie Music, Busking & Underground)",
                                        "city_seoul",
                                    ),
                                    (
                                        "distr_yongsan",
                                        "Yongsan (HYBE HQ Complex)",
                                        "city_seoul",
                                    ),
                                ],
                            }
                        ],
                    }
                ],
            },
            # NIGERIA
            {
                "country": ("geo_ng", "Nigeria", "Africa"),
                "states": [
                    {
                        "state": ("state_ng_lagos", "Lagos State", "Nigeria"),
                        "cities": [
                            {
                                "city": (
                                    "city_lagos",
                                    "Lagos",
                                    "state_ng_lagos",
                                    "Nigeria",
                                ),
                                "districts": [
                                    (
                                        "distr_lekki",
                                        "Lekki & Victoria Island (Afrobeats Creative Hub)",
                                        "city_lagos",
                                    ),
                                    (
                                        "distr_ikeja",
                                        "Ikeja (Kalakuta Shrine & Fela Legacy)",
                                        "city_lagos",
                                    ),
                                ],
                            }
                        ],
                    }
                ],
            },
            # JAMAICA
            {
                "country": ("geo_jm", "Jamaica", "Caribbean"),
                "states": [
                    {
                        "state": ("state_jm_kingston", "Kingston Parish", "Jamaica"),
                        "cities": [
                            {
                                "city": (
                                    "city_kingston",
                                    "Kingston",
                                    "state_jm_kingston",
                                    "Jamaica",
                                ),
                                "districts": [
                                    (
                                        "distr_trenchtown",
                                        "Trenchtown (Roots Reggae Birthplace)",
                                        "city_kingston",
                                    ),
                                    (
                                        "distr_waterhouse",
                                        "Waterhouse (King Tubby Dub Studio)",
                                        "city_kingston",
                                    ),
                                ],
                            }
                        ],
                    }
                ],
            },
        ]

        # Ingest Geo-Spatial Entities & Hierarchy Edges
        for country_block in geo_tree:
            cid, cname, cont = country_block["country"]
            c_ent = BaseEntity(
                id=cid,
                name=cname,
                entity_type=EntityType.PRODUCTION_HOUSE,
                attributes={"category": "Country", "continent": cont},
            )
            add_ent(c_ent)

            for state_block in country_block["states"]:
                sid, sname, _ = state_block["state"]
                s_ent = BaseEntity(
                    id=sid,
                    name=sname,
                    entity_type=EntityType.PRODUCTION_HOUSE,
                    attributes={"category": "State/Region", "country": cname},
                )
                add_ent(s_ent)
                edges.append(
                    RelationshipEdge(
                        source_id=sid,
                        target_id=cid,
                        rel_type="PARENT_COMPANY_OF",
                        weight=1.0,
                        metadata={"hierarchy": "state_to_country"},
                    )
                )

                for city_block in state_block["cities"]:
                    city_id, city_name, _, _ = city_block["city"]
                    city_ent = BaseEntity(
                        id=city_id,
                        name=city_name,
                        entity_type=EntityType.PRODUCTION_HOUSE,
                        attributes={
                            "category": "City/Hub",
                            "state": sname,
                            "country": cname,
                        },
                    )
                    add_ent(city_ent)
                    edges.append(
                        RelationshipEdge(
                            source_id=city_id,
                            target_id=sid,
                            rel_type="PARENT_COMPANY_OF",
                            weight=1.0,
                            metadata={"hierarchy": "city_to_state"},
                        )
                    )

                    for d_id, d_name, _ in city_block["districts"]:
                        d_ent = BaseEntity(
                            id=d_id,
                            name=d_name,
                            entity_type=EntityType.PRODUCTION_HOUSE,
                            attributes={
                                "category": "Creative District",
                                "city": city_name,
                            },
                        )
                        add_ent(d_ent)
                        edges.append(
                            RelationshipEdge(
                                source_id=d_id,
                                target_id=city_id,
                                rel_type="PARENT_COMPANY_OF",
                                weight=1.0,
                                metadata={"hierarchy": "district_to_city"},
                            )
                        )

        # =========================================================================
        # 2. MUSICAL GENRE & SUBGENRE & MICRO-SCENE TAXONOMY
        # =========================================================================
        genre_tree = [
            # Root: Electronic Music
            ("tax_electronic", "Electronic Music", "Root Genre", None, None),
            ("tax_techno", "Techno", "Subgenre", "tax_electronic", "city_detroit"),
            (
                "tax_industrial_techno",
                "Industrial Techno / Berghain Sound",
                "Micro-Genre",
                "tax_techno",
                "distr_fhain_xberg",
            ),
            (
                "tax_melodic_techno",
                "Melodic & Peak-Time Techno",
                "Micro-Genre",
                "tax_techno",
                "city_berlin",
            ),
            (
                "tax_krautrock_synth",
                "Krautrock & Berlin School Synthesizer",
                "Micro-Genre",
                "tax_electronic",
                "distr_duss_altstadt",
            ),
            (
                "tax_house",
                "House Music",
                "Subgenre",
                "tax_electronic",
                "distr_southside_chi",
            ),
            (
                "tax_french_touch",
                "French Touch / Nu-Disco Filter",
                "Micro-Genre",
                "tax_house",
                "distr_pigalle",
            ),
            (
                "tax_deep_house",
                "Deep House",
                "Micro-Genre",
                "tax_house",
                "city_chicago",
            ),
            ("tax_amapiano", "Amapiano", "Micro-Genre", "tax_house", "city_lagos"),
            (
                "tax_trance",
                "Trance Music",
                "Subgenre",
                "tax_electronic",
                "distr_sachsenhausen",
            ),
            (
                "tax_idm",
                "Intelligent Dance Music (IDM) & Braindance",
                "Micro-Genre",
                "tax_electronic",
                "distr_soho_london",
            ),
            (
                "tax_dnb",
                "Drum & Bass / Jungle",
                "Subgenre",
                "tax_electronic",
                "distr_hackney",
            ),
            # Root: Pop & Urban
            ("tax_pop_urban", "Pop & Urban Music", "Root Genre", None, None),
            (
                "tax_nordic_pop",
                "Nordic Pop Architecture",
                "Subgenre",
                "tax_pop_urban",
                "distr_ostermalm",
            ),
            (
                "tax_kpop",
                "K-Pop Industry Standard",
                "Subgenre",
                "tax_pop_urban",
                "distr_gangnam",
            ),
            (
                "tax_jpop",
                "J-Pop & Shibuya-kei",
                "Subgenre",
                "tax_pop_urban",
                "distr_shibuya",
            ),
            (
                "tax_afrobeats",
                "Afrobeats & Afro-Fusion",
                "Subgenre",
                "tax_pop_urban",
                "distr_lekki",
            ),
            (
                "tax_reggae_dub",
                "Reggae & Roots Dub",
                "Subgenre",
                "tax_pop_urban",
                "distr_trenchtown",
            ),
            (
                "tax_latin_trap",
                "Latin Trap & Reggaeton",
                "Subgenre",
                "tax_pop_urban",
                "city_la",
            ),
            # Root: Hip-Hop
            ("tax_hiphop", "Hip-Hop", "Root Genre", None, "distr_bronx"),
            (
                "tax_westcoast_gfunk",
                "West Coast G-Funk",
                "Subgenre",
                "tax_hiphop",
                "distr_compton",
            ),
            (
                "tax_atlanta_trap",
                "Atlanta Trap",
                "Subgenre",
                "tax_hiphop",
                "distr_buckhead_atl",
            ),
            (
                "tax_toronto_sound",
                "Toronto Sound / Dark R&B",
                "Subgenre",
                "tax_hiphop",
                "city_nyc",
            ),
            # Root: Rock & Alternative
            ("tax_rock_alt", "Rock & Alternative", "Root Genre", None, None),
            (
                "tax_grunge",
                "Seattle Grunge",
                "Subgenre",
                "tax_rock_alt",
                "distr_caphill_sea",
            ),
            (
                "tax_britpop",
                "Britpop & Madchester",
                "Subgenre",
                "tax_rock_alt",
                "distr_nq_mcr",
            ),
            (
                "tax_post_punk",
                "Post-Punk & New Wave",
                "Subgenre",
                "tax_rock_alt",
                "distr_soho_london",
            ),
            (
                "tax_trip_hop",
                "Bristol Trip-Hop Sound",
                "Subgenre",
                "tax_rock_alt",
                "distr_stpauls_bristol",
            ),
            # Root: Classical & Cinematic
            (
                "tax_classical_cinema",
                "Classical & Cinematic Scoring",
                "Root Genre",
                None,
                None,
            ),
            (
                "tax_post_minimalism",
                "Post-Minimalism & Neo-Classical",
                "Subgenre",
                "tax_classical_cinema",
                "distr_treptow",
            ),
            (
                "tax_cinematic_hollywood",
                "Hollywood Orchestral Film Scoring",
                "Subgenre",
                "tax_classical_cinema",
                "distr_hollywood",
            ),
        ]

        for gid, gname, glevel, parent_id, origin_scene in genre_tree:
            g_ent = BaseEntity(
                id=gid,
                name=gname,
                entity_type=EntityType.TRACK,  # Taxonomy entity
                attributes={
                    "category": "Genre Taxonomy (arXiv:2110.08862)",
                    "taxonomy_level": glevel,
                    "origin_scene": origin_scene,
                },
            )
            add_ent(g_ent)

            if parent_id:
                edges.append(
                    RelationshipEdge(
                        source_id=gid,
                        target_id=parent_id,
                        rel_type="PARENT_COMPANY_OF",
                        weight=1.0,
                        metadata={"hierarchy": "subgenre_to_parent"},
                    )
                )

            if origin_scene:
                edges.append(
                    RelationshipEdge(
                        source_id=gid,
                        target_id=origin_scene,
                        rel_type="RECORDED_AT",
                        weight=0.95,
                        metadata={"origin_link": "birthplace_scene"},
                    )
                )

        return entities, edges
