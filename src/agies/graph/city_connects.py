"""City-Level Industry Connects & Inter-City Corridor Engine.

Enriches the Knowledge Graph with explicit city-level industry infrastructure:
1. Local Industry Anchors (Artists, Studios, Labels, Agencies, Festivals tied to Cities)
2. City Industry Power Profiles & Infrastructure Scoring
3. Inter-City Creative Corridors (e.g. Stockholm <-> LA Pop Highway, Berlin <-> London Club Pipeline, Kingston <-> London Dub Line)
"""

import logging
from typing import Any, Dict, List, Tuple

from agies.graph.builder import MusicIndustryGraph
from agies.graph.schema import (
    EntityType,
)

logger = logging.getLogger("agies.graph.city_connects")


class CityIndustryConnectsEnricher:
    """Enriches graph with comprehensive city-level industry anchors and inter-city corridors."""

    CITY_ANCHORS_MAP: List[Tuple[str, str, str]] = [
        # (Entity ID, City ID, Relationship Type)
        # === BERLIN ===
        ("art_kraftwerk", "city_berlin", "RECORDED_AT"),
        ("art_davidbowie", "city_berlin", "RECORDED_AT"),
        ("art_depechemode", "city_berlin", "RECORDED_AT"),
        ("art_nilsfrahm_art", "city_berlin", "BASED_IN_CITY"),
        ("art_modeselektor", "city_berlin", "BASED_IN_CITY"),
        ("art_stephanbodzin_art", "city_berlin", "BASED_IN_CITY"),
        ("art_paulvandyk_art", "city_berlin", "BASED_IN_CITY"),
        ("art_borisbrejcha", "city_berlin", "BASED_IN_CITY"),
        ("std_hansa", "city_berlin", "OPERATES_IN_CITY"),
        ("std_funkhaus", "city_berlin", "OPERATES_IN_CITY"),
        ("std_teldex", "city_berlin", "OPERATES_IN_CITY"),
        ("std_emilberliner", "city_berlin", "OPERATES_IN_CITY"),
        ("lbl_ostgut", "city_berlin", "HEADQUARTERED_IN"),
        ("lbl_tresor", "city_berlin", "HEADQUARTERED_IN"),
        ("lbl_innervisions", "city_berlin", "HEADQUARTERED_IN"),
        ("lbl_boysnoize", "city_berlin", "HEADQUARTERED_IN"),
        ("lbl_dg", "city_berlin", "HEADQUARTERED_IN"),
        ("gate_colors", "city_berlin", "HEADQUARTERED_IN"),
        ("prd_nilsfrahm", "city_berlin", "ANCHOR_PRODUCER_OF"),
        ("prd_boysnoize", "city_berlin", "ANCHOR_PRODUCER_OF"),
        ("prd_stephanbodzin", "city_berlin", "ANCHOR_PRODUCER_OF"),
        # === COLOGNE & DÜSSELDORF ===
        ("lbl_kompakt", "city_cologne", "HEADQUARTERED_IN"),
        ("fest_copop", "city_cologne", "HOSTED_IN_CITY"),
        ("std_klingklang", "city_dusseldorf", "OPERATES_IN_CITY"),
        ("prd_connyplank", "city_cologne", "ANCHOR_PRODUCER_OF"),
        # === HAMBURG ===
        ("fest_reeperbahn", "city_hamburg", "HOSTED_IN_CITY"),
        ("lbl_warner_rec", "city_hamburg", "OPERATES_IN_CITY"),
        # === LONDON ===
        ("art_beatles", "city_london", "RECORDED_AT"),
        ("art_queen", "city_london", "BASED_IN_CITY"),
        ("art_radiohead", "city_london", "RECORDED_AT"),
        ("art_adele", "city_london", "BASED_IN_CITY"),
        ("art_dua", "city_london", "BASED_IN_CITY"),
        ("art_harry", "city_london", "BASED_IN_CITY"),
        ("art_aphex", "city_london", "BASED_IN_CITY"),
        ("art_fourtet", "city_london", "BASED_IN_CITY"),
        ("art_bicep", "city_london", "BASED_IN_CITY"),
        ("std_abbey", "city_london", "OPERATES_IN_CITY"),
        ("std_air", "city_london", "OPERATES_IN_CITY"),
        ("std_metropolis", "city_london", "OPERATES_IN_CITY"),
        ("std_rak", "city_london", "OPERATES_IN_CITY"),
        ("lbl_beggars", "city_london", "HEADQUARTERED_IN"),
        ("lbl_4ad", "city_london", "HEADQUARTERED_IN"),
        ("lbl_xl_rec", "city_london", "HEADQUARTERED_IN"),
        ("lbl_rough_trade", "city_london", "HEADQUARTERED_IN"),
        ("lbl_warp", "city_london", "HEADQUARTERED_IN"),
        ("lbl_ninja_tune", "city_london", "HEADQUARTERED_IN"),
        ("lbl_domino", "city_london", "HEADQUARTERED_IN"),
        ("lbl_parlophone", "city_london", "HEADQUARTERED_IN"),
        ("gate_bbc_intro", "city_london", "HEADQUARTERED_IN"),
        ("gate_boilerroom", "city_london", "HEADQUARTERED_IN"),
        ("rights_prs", "city_london", "HEADQUARTERED_IN"),
        ("prd_brian", "city_london", "ANCHOR_PRODUCER_OF"),
        ("prd_georgemartin", "city_london", "ANCHOR_PRODUCER_OF"),
        # === LOS ANGELES ===
        ("art_billie", "city_la", "BASED_IN_CITY"),
        ("art_kendrick", "city_la", "BASED_IN_CITY"),
        ("art_eminem", "city_la", "RECORDED_AT"),
        ("art_travisscott", "city_la", "RECORDED_AT"),
        ("art_redhot", "city_la", "BASED_IN_CITY"),
        ("art_skrillex_art", "city_la", "BASED_IN_CITY"),
        ("art_flyinglotus", "city_la", "BASED_IN_CITY"),
        ("std_sunset", "city_la", "OPERATES_IN_CITY"),
        ("std_conway", "city_la", "OPERATES_IN_CITY"),
        ("std_capitol", "city_la", "OPERATES_IN_CITY"),
        ("std_soundcity", "city_la", "OPERATES_IN_CITY"),
        ("lbl_interscope", "city_la", "HEADQUARTERED_IN"),
        ("lbl_capitol", "city_la", "HEADQUARTERED_IN"),
        ("lbl_topdawg", "city_la", "HEADQUARTERED_IN"),
        ("lbl_pglang", "city_la", "HEADQUARTERED_IN"),
        ("lbl_brainfeeder", "city_la", "HEADQUARTERED_IN"),
        ("lbl_stones_throw", "city_la", "HEADQUARTERED_IN"),
        ("ag_wme", "city_la", "HEADQUARTERED_IN"),
        ("ag_caa", "city_la", "HEADQUARTERED_IN"),
        ("ag_uta", "city_la", "HEADQUARTERED_IN"),
        ("prd_drdre", "city_la", "ANCHOR_PRODUCER_OF"),
        ("prd_finneas", "city_la", "ANCHOR_PRODUCER_OF"),
        ("prd_rick", "city_la", "ANCHOR_PRODUCER_OF"),
        # === NEW YORK CITY ===
        ("art_kanye", "city_nyc", "RECORDED_AT"),
        ("art_taylor", "city_nyc", "RECORDED_AT"),
        ("art_sza", "city_nyc", "RECORDED_AT"),
        ("std_electric", "city_nyc", "OPERATES_IN_CITY"),
        ("lbl_republic", "city_nyc", "HEADQUARTERED_IN"),
        ("lbl_def_jam", "city_nyc", "HEADQUARTERED_IN"),
        ("lbl_columbia", "city_nyc", "HEADQUARTERED_IN"),
        ("lbl_rca", "city_nyc", "HEADQUARTERED_IN"),
        ("lbl_atlantic", "city_nyc", "HEADQUARTERED_IN"),
        ("lbl_rocnation_lbl", "city_nyc", "HEADQUARTERED_IN"),
        ("ag_rocnation", "city_nyc", "HEADQUARTERED_IN"),
        ("prd_jack", "city_nyc", "ANCHOR_PRODUCER_OF"),
        ("rights_ascap", "city_nyc", "HEADQUARTERED_IN"),
        # === STOCKHOLM ===
        ("art_abba", "city_stockholm", "BASED_IN_CITY"),
        ("art_avicii", "city_stockholm", "BASED_IN_CITY"),
        ("art_swedishhouse", "city_stockholm", "BASED_IN_CITY"),
        ("art_robyn", "city_stockholm", "BASED_IN_CITY"),
        ("art_zaralarsson", "city_stockholm", "BASED_IN_CITY"),
        ("std_maratone", "city_stockholm", "OPERATES_IN_CITY"),
        ("lbl_mxm_prod", "city_stockholm", "HEADQUARTERED_IN"),
        ("lbl_ten_music", "city_stockholm", "HEADQUARTERED_IN"),
        ("prd_max", "city_stockholm", "ANCHOR_PRODUCER_OF"),
        ("prd_shellback", "city_stockholm", "ANCHOR_PRODUCER_OF"),
        ("prd_goransson", "city_stockholm", "ANCHOR_PRODUCER_OF"),
        # === PARIS ===
        ("art_daftpunk", "city_paris", "BASED_IN_CITY"),
        ("art_justice", "city_paris", "BASED_IN_CITY"),
        ("art_phoenix", "city_paris", "BASED_IN_CITY"),
        ("art_air_band", "city_paris", "BASED_IN_CITY"),
        ("art_davidguetta", "city_paris", "BASED_IN_CITY"),
        ("art_gesaffelstein", "city_paris", "BASED_IN_CITY"),
        ("std_motorbass", "city_paris", "OPERATES_IN_CITY"),
        ("std_grandearmee", "city_paris", "OPERATES_IN_CITY"),
        ("lbl_edbanger", "city_paris", "HEADQUARTERED_IN"),
        ("lbl_because", "city_paris", "HEADQUARTERED_IN"),
        ("gate_cercle", "city_paris", "HEADQUARTERED_IN"),
        ("prd_daft_thomas", "city_paris", "ANCHOR_PRODUCER_OF"),
        ("prd_pedrowinter", "city_paris", "ANCHOR_PRODUCER_OF"),
        # === TOKYO ===
        ("art_ymo", "city_tokyo", "BASED_IN_CITY"),
        ("art_sakamoto", "city_tokyo", "BASED_IN_CITY"),
        ("art_hisaishi", "city_tokyo", "BASED_IN_CITY"),
        ("art_nujabes", "city_tokyo", "BASED_IN_CITY"),
        ("art_babymetal", "city_tokyo", "BASED_IN_CITY"),
        ("std_sonytokyo", "city_tokyo", "OPERATES_IN_CITY"),
        ("std_ghibli", "city_tokyo", "OPERATES_IN_CITY"),
        ("lbl_avex", "city_tokyo", "HEADQUARTERED_IN"),
        ("lbl_sony_japan", "city_tokyo", "HEADQUARTERED_IN"),
        ("prd_sakamoto_prd", "city_tokyo", "ANCHOR_PRODUCER_OF"),
        ("prd_hisaishi_prd", "city_tokyo", "ANCHOR_PRODUCER_OF"),
        # === SEOUL ===
        ("art_bts", "city_seoul", "BASED_IN_CITY"),
        ("art_blackpink", "city_seoul", "BASED_IN_CITY"),
        ("art_newjeans", "city_seoul", "BASED_IN_CITY"),
        ("art_straykids", "city_seoul", "BASED_IN_CITY"),
        ("art_seventeen", "city_seoul", "BASED_IN_CITY"),
        ("std_hybe_std", "city_seoul", "OPERATES_IN_CITY"),
        ("lbl_hybe_corp", "city_seoul", "HEADQUARTERED_IN"),
        ("lbl_sm_ent", "city_seoul", "HEADQUARTERED_IN"),
        ("lbl_yg_ent", "city_seoul", "HEADQUARTERED_IN"),
        ("lbl_jyp_ent", "city_seoul", "HEADQUARTERED_IN"),
        ("prd_hitman", "city_seoul", "ANCHOR_PRODUCER_OF"),
        ("prd_teddypark", "city_seoul", "ANCHOR_PRODUCER_OF"),
        ("prd_pdogg", "city_seoul", "ANCHOR_PRODUCER_OF"),
        # === LAGOS ===
        ("art_felakuti", "city_lagos", "BASED_IN_CITY"),
        ("art_burnaboy", "city_lagos", "BASED_IN_CITY"),
        ("art_wizkid", "city_lagos", "BASED_IN_CITY"),
        ("art_davido", "city_lagos", "BASED_IN_CITY"),
        ("art_tems", "city_lagos", "BASED_IN_CITY"),
        ("art_rema", "city_lagos", "BASED_IN_CITY"),
        ("std_mavin_std", "city_lagos", "OPERATES_IN_CITY"),
        ("lbl_mavin", "city_lagos", "HEADQUARTERED_IN"),
        ("lbl_starboy", "city_lagos", "HEADQUARTERED_IN"),
        ("lbl_spaceship", "city_lagos", "HEADQUARTERED_IN"),
        ("lbl_ybnl", "city_lagos", "HEADQUARTERED_IN"),
        ("prd_donjazzy", "city_lagos", "ANCHOR_PRODUCER_OF"),
        ("prd_sarz", "city_lagos", "ANCHOR_PRODUCER_OF"),
        # === KINGSTON ===
        ("art_bobmarley", "city_kingston", "BASED_IN_CITY"),
        ("art_kingtubby_art", "city_kingston", "BASED_IN_CITY"),
        ("art_leeperry_art", "city_kingston", "BASED_IN_CITY"),
        ("art_seanpaul", "city_kingston", "BASED_IN_CITY"),
        ("std_tuffgong", "city_kingston", "OPERATES_IN_CITY"),
        ("std_blackark", "city_kingston", "OPERATES_IN_CITY"),
        ("lbl_tuffgong_lbl", "city_kingston", "HEADQUARTERED_IN"),
        ("lbl_studio_one", "city_kingston", "HEADQUARTERED_IN"),
        ("prd_kingtubby", "city_kingston", "ANCHOR_PRODUCER_OF"),
        ("prd_leeperry", "city_kingston", "ANCHOR_PRODUCER_OF"),
        # === ATLANTA ===
        ("art_future", "city_atlanta", "BASED_IN_CITY"),
        ("art_21savage", "city_atlanta", "BASED_IN_CITY"),
        ("lbl_qc", "city_atlanta", "HEADQUARTERED_IN"),
        ("prd_metro", "city_atlanta", "ANCHOR_PRODUCER_OF"),
        # === SEATTLE ===
        ("art_nirvana", "city_seattle", "BASED_IN_CITY"),
        ("art_foo", "city_seattle", "BASED_IN_CITY"),
        ("lbl_sub_pop", "city_seattle", "HEADQUARTERED_IN"),
        ("prd_butch", "city_seattle", "ANCHOR_PRODUCER_OF"),
        # === NASHVILLE ===
        ("std_oceanway", "city_nashville", "OPERATES_IN_CITY"),
        ("std_blackbird", "city_nashville", "OPERATES_IN_CITY"),
        # === SÃO PAULO & RIO DE JANEIRO & ITAJAÍ ===
        ("art_alok", "city_saopaulo", "BASED_IN_CITY"),
        ("art_vintageculture", "city_saopaulo", "BASED_IN_CITY"),
        ("art_amontobin", "city_saopaulo", "BASED_IN_CITY"),
        ("art_anitta", "city_riodejaneiro", "BASED_IN_CITY"),
        ("lbl_dedge_rec", "city_saopaulo", "HEADQUARTERED_IN"),
        ("std_warung_std", "city_itajai", "OPERATES_IN_CITY"),
        # === MEDELLÍN & BOGOTÁ ===
        ("art_jbalvin", "city_medellin", "BASED_IN_CITY"),
        ("art_maluma", "city_medellin", "BASED_IN_CITY"),
        ("art_karolg", "city_medellin", "BASED_IN_CITY"),
        ("std_infinitymusic", "city_medellin", "OPERATES_IN_CITY"),
        ("lbl_latino_gang", "city_medellin", "HEADQUARTERED_IN"),
        ("lbl_baum_rec", "city_bogota", "HEADQUARTERED_IN"),
        # === MEXICO CITY ===
        ("art_natanaelcano", "city_cdmx", "BASED_IN_CITY"),
        ("art_pesopluma", "city_cdmx", "BASED_IN_CITY"),
        ("lbl_rancho_humilde", "city_cdmx", "HEADQUARTERED_IN"),
        ("fest_mutek_mx", "city_cdmx", "HOSTED_IN_CITY"),
        # === BARCELONA & IBIZA ===
        ("art_rosalia", "city_barcelona", "BASED_IN_CITY"),
        ("art_elguincho", "city_barcelona", "BASED_IN_CITY"),
        ("fest_sonar", "city_barcelona", "HOSTED_IN_CITY"),
        ("fest_primavera", "city_barcelona", "HOSTED_IN_CITY"),
        ("lbl_elrow_music", "city_barcelona", "HEADQUARTERED_IN"),
        ("lbl_dc10_rec", "city_ibiza", "HEADQUARTERED_IN"),
        # === AMSTERDAM ===
        ("art_armin", "city_amsterdam", "BASED_IN_CITY"),
        ("art_tiesto", "city_amsterdam", "BASED_IN_CITY"),
        ("art_martingarrix", "city_amsterdam", "BASED_IN_CITY"),
        ("fest_ade", "city_amsterdam", "HOSTED_IN_CITY"),
        ("fest_dekmantel", "city_amsterdam", "HOSTED_IN_CITY"),
        ("lbl_spinnin", "city_amsterdam", "HEADQUARTERED_IN"),
        ("lbl_armada", "city_amsterdam", "HEADQUARTERED_IN"),
        # === MELBOURNE & SYDNEY ===
        ("art_tameimpala", "city_melbourne", "BASED_IN_CITY"),
        ("art_flume", "city_sydney", "BASED_IN_CITY"),
        ("art_rufusdusol", "city_sydney", "BASED_IN_CITY"),
        ("lbl_futureclassic", "city_sydney", "HEADQUARTERED_IN"),
        # === JOHANNESBURG ===
        ("art_blackcoffee", "city_joburg", "BASED_IN_CITY"),
        ("art_kabzadesmall", "city_joburg", "BASED_IN_CITY"),
        ("art_djmaphorisa", "city_joburg", "BASED_IN_CITY"),
        ("lbl_soulistic", "city_joburg", "HEADQUARTERED_IN"),
        ("lbl_piano_hub", "city_joburg", "HEADQUARTERED_IN"),
        # === GOA & MUMBAI ===
        ("art_arrahman", "city_mumbai", "BASED_IN_CITY"),
        ("art_nucleya", "city_goa", "BASED_IN_CITY"),
        ("lbl_tseries", "city_mumbai", "HEADQUARTERED_IN"),
        ("lbl_azadi_records", "city_mumbai", "HEADQUARTERED_IN"),
        # === BRUSSELS ===
        ("art_stromae", "city_brussels", "BASED_IN_CITY"),
        ("art_charlottedewitte", "city_brussels", "BASED_IN_CITY"),
        ("art_amelielens", "city_brussels", "BASED_IN_CITY"),
        ("lbl_kntxt", "city_brussels", "HEADQUARTERED_IN"),
        ("lbl_lenske", "city_brussels", "HEADQUARTERED_IN"),
    ]

    INTER_CITY_CORRIDORS: List[Tuple[str, str, str, float]] = [
        # (City 1, City 2, Corridor Name, Strength Weight)
        ("city_berlin", "city_london", "European Electronic & Club Highway", 0.98),
        ("city_stockholm", "city_la", "Transatlantic Pop Hitmaking Axis", 0.99),
        ("city_london", "city_la", "Anglo-American Major Label Corridor", 0.97),
        (
            "city_kingston",
            "city_london",
            "Historical Dub, Bass & Sound System Line",
            0.96,
        ),
        (
            "city_lagos",
            "city_london",
            "Afrobeats Global Mainstream Pipeline",
            0.98,
        ),
        ("city_seoul", "city_la", "K-Pop & American Visual Media Super-Corridor", 0.95),
        ("city_paris", "city_london", "French Touch & Electronic Trade Channel", 0.94),
        ("city_cologne", "city_berlin", "Kompakt-Ostgut German Minimal Techno Line", 0.93),
        ("city_la", "city_nyc", "US Coast-to-Coast Major Label Duopoly", 0.98),
        ("city_kingston", "city_nyc", "Caribbean Sound to East Coast Rap Bridge", 0.90),
        ("city_tokyo", "city_la", "Japanese Soundtracks to Hollywood Scoring Bridge", 0.88),
        ("city_saopaulo", "city_berlin", "São Paulo ↔ Berlin Industrial Techno Axis", 0.95),
        ("city_medellin", "city_la", "Medellín ↔ LA Global Latin Urban Highway", 0.97),
        ("city_joburg", "city_london", "Johannesburg ↔ London Amapiano Diaspora Line", 0.98),
        ("city_barcelona", "city_amsterdam", "Barcelona ↔ Amsterdam Sónar-ADE Festival Super-Corridor", 0.99),
        ("city_melbourne", "city_berlin", "Melbourne ↔ Berlin Minimal & Underground Club Channel", 0.94),
        ("city_ibiza", "city_london", "Ibiza ↔ London Seasonal Club Residency Pipeline", 0.98),
        ("city_mumbai", "city_london", "Mumbai ↔ London South Asian Diaspora & UK Bass Axis", 0.93),
        ("city_brussels", "city_berlin", "Brussels ↔ Berlin Peak-Time Techno Pipeline", 0.96),
        ("city_detroit", "city_berlin", "Transatlantic Techno Sister City Bridge", 0.99),
    ]

    def enrich_city_connects(
        self, industry_graph: MusicIndustryGraph
    ) -> Dict[str, Any]:
        """Inject explicit city-level industry infrastructure and inter-city corridors."""
        graph = industry_graph.graph
        added_anchors_count = 0
        added_corridors_count = 0

        # 1. Connect entities to their city nodes
        for ent_id, city_id, rel_type in self.CITY_ANCHORS_MAP:
            if ent_id in graph and city_id in graph:
                if not graph.has_edge(ent_id, city_id):
                    graph.add_edge(
                        ent_id,
                        city_id,
                        rel_type=rel_type,
                        weight=1.0,
                        is_city_anchor=True,
                    )
                    added_anchors_count += 1

        # 2. Add Inter-City Creative Corridors
        for c1, c2, corridor_name, weight in self.INTER_CITY_CORRIDORS:
            if c1 in graph and c2 in graph:
                if not graph.has_edge(c1, c2):
                    graph.add_edge(
                        c1,
                        c2,
                        rel_type="COLLABORATED_WITH",
                        corridor_name=corridor_name,
                        weight=weight,
                        is_city_corridor=True,
                    )
                    added_corridors_count += 1

        logger.info(
            "Enriched City Connects: %d city infrastructure anchors and %d inter-city corridors added.",
            added_anchors_count,
            added_corridors_count,
        )

        return {
            "city_anchors_added": added_anchors_count,
            "inter_city_corridors_added": added_corridors_count,
        }

    def get_city_profile(
        self, industry_graph: MusicIndustryGraph, city_id: str
    ) -> Dict[str, Any]:
        """Compute full industry ecosystem breakdown for a given city."""
        graph = industry_graph.graph
        if city_id not in graph:
            raise KeyError(f"City '{city_id}' not found in knowledge graph.")

        cdata = graph.nodes[city_id]
        city_name = cdata.get("name", city_id)

        artists, studios, labels, producers, agencies, festivals, corridors = (
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        )

        # Find all nodes connected to this city
        for u, v, d in graph.edges(data=True):
            if v == city_id or u == city_id:
                other_id = u if v == city_id else v
                other_data = graph.nodes.get(other_id, {})
                etype = other_data.get("entity_type")
                name = other_data.get("name", other_id)

                if d.get("is_city_corridor"):
                    corridors.append(
                        {
                            "connected_city": name,
                            "corridor_name": d.get("corridor_name"),
                            "strength": d.get("weight"),
                        }
                    )
                elif etype == EntityType.ARTIST.value or etype == "artist":
                    artists.append(
                        {
                            "id": other_id,
                            "name": name,
                            "genres": other_data.get("genres", []),
                        }
                    )
                elif etype == EntityType.STUDIO.value or etype == "studio":
                    studios.append(
                        {
                            "id": other_id,
                            "name": name,
                            "tier": other_data.get("equipment_tier"),
                        }
                    )
                elif etype == EntityType.RECORD_LABEL.value or etype == "record_label":
                    labels.append(
                        {
                            "id": other_id,
                            "name": name,
                            "is_major": other_data.get("is_major", False),
                        }
                    )
                elif etype == EntityType.PRODUCER.value or etype == "producer":
                    producers.append(
                        {"id": other_id, "name": name, "role": other_data.get("role")}
                    )
                elif "festival" in other_id or "fest_" in other_id:
                    festivals.append({"id": other_id, "name": name})
                elif etype == EntityType.AGENCY.value or etype == "agency":
                    agencies.append({"id": other_id, "name": name})

        # Calculate City Infrastructure Power Score
        power_score = round(
            len(studios) * 3.0
            + len(labels) * 2.5
            + len(producers) * 2.0
            + len(artists) * 1.5
            + len(festivals) * 3.0,
            1,
        )

        return {
            "city_id": city_id,
            "city_name": city_name,
            "state_country": cdata.get("attributes", {}).get("country", "Global"),
            "infrastructure_power_score": power_score,
            "anchored_artists_count": len(artists),
            "studios_count": len(studios),
            "labels_count": len(labels),
            "producers_count": len(producers),
            "festivals_count": len(festivals),
            "artists": artists,
            "studios": studios,
            "record_labels": labels,
            "producers": producers,
            "festivals_and_gateways": festivals,
            "inter_city_corridors": corridors,
        }
