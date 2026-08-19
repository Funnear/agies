"""Graph Density & Multi-Dimensional Inclusion Engine.

Dramatically increases Knowledge Graph density via structural, acoustic,
and institutional inclusion closures:
1. Shared Acoustic Studio Spaces (Artists sharing recording rooms & consoles)
2. Label Roster Fellowships (Label-mates & distribution partnerships)
3. Hardware Synthesizer & Analog Gear Footprints (Moog, Roland, Prophet, Neve, SSL)
4. Sound System Calibration (Funktion-One, d&b audiotechnik, L-Acoustics)
5. Inter-City Corridor Clustering & Scene Peer Networks
6. Cross-Genre Ancestral & Hybrid Influences
7. Festival & A&R Showcase Lineup Inclusions
"""

from collections import defaultdict
import logging
from typing import Any, Dict, List, Tuple

from agies.graph.builder import MusicIndustryGraph
from agies.graph.schema import (
    BaseEntity,
    EntityType,
)

logger = logging.getLogger("agies.graph.density")


class GraphDensityInclusionEngine:
    """Enriches the Knowledge Graph with dense multi-layer inclusion closures."""

    HARDWARE_GEAR_CORPUS: List[Tuple[str, str, str, str]] = [
        # (Gear ID, Name, Category, Acoustic Signature)
        ("gear_moog_sub37", "Moog Sub 37 Analog Synthesizer", "Analog Monosynth", "Warm ladder filter sub-harmonics"),
        ("gear_space_echo_re201", "Roland Space Echo RE-201 Tape Delay", "Analog Tape Echo", "Warm spring reverb & tape flutter"),
        ("gear_tb303", "Roland TB-303 Bass Line", "Bass Synthesizer", "Resonant acid squelch & diode ladder filter"),
        ("gear_tr808", "Roland TR-808 Rhythm Composer", "Analog Drum Machine", "Booming sub-bass kick & crisp snare"),
        ("gear_tr909", "Roland TR-909 Rhythm Composer", "Analog/PCM Drum Machine", "Punchy 4-on-the-floor techno kick"),
        ("gear_prophet6", "Sequential Prophet-6 Analog Polyphonic", "Analog Polysynth", "Lush brassy pads & modern modulation"),
        ("gear_ob6", "Dave Smith Instruments OB-6", "SEM Filter Polysynth", "Oberheim creamy 12dB multi-mode filters"),
        ("gear_dx7", "Yamaha DX7 FM Synthesizer", "Digital FM Synthesizer", "Iconic glassy 80s electric pianos & chimes"),
        ("gear_ssl4000", "Solid State Logic SSL 4000 G+ Console", "Mixing Console", "Punchy VCA bus compressor & British EQ"),
        ("gear_neve8078", "Neve 8078 Discrete Analogue Console", "Recording Console", "Massive harmonic saturation & 31105 preamps"),
        ("gear_studer_a800", "Studer A800 24-Track Tape Recorder", "Analog Tape Machine", "Rich 2-inch tape compression & glue"),
        ("gear_funktion_one", "Funktion-One Resolution 5 Sound System", "Club PA Sound System", "Horn-loaded natural point-source fidelity"),
        ("gear_dnb_soundscape", "d&b audiotechnik Soundscape Immersive", "Acoustic System", "Object-based spatial immersive soundfield"),
        ("gear_lacoustics_k2", "L-Acoustics K2 Line Source Array", "Concert PA System", "Smooth high-frequency wave-sculpting"),
    ]

    GEAR_USAGE_MAP: List[Tuple[str, str, str]] = [
        # (Artist/Studio/Venue ID, Gear ID, Relationship)
        # Nils Frahm
        ("art_nilsfrahm", "gear_space_echo_re201", "PRIMARY_ACOUSTIC_INSTRUMENT"),
        ("art_nilsfrahm", "gear_moog_sub37", "STUDIO_HARDWARE_SYNTH"),
        ("art_nilsfrahm_art", "gear_space_echo_re201", "PRIMARY_ACOUSTIC_INSTRUMENT"),
        ("std_funkhaus", "gear_space_echo_re201", "INSTALLED_STUDIO_GEAR"),
        ("std_funkhaus", "gear_dnb_soundscape", "ACOUSTIC_SYSTEM_INSTALLED"),
        # Stephan Bodzin
        ("art_stephanbodzin", "gear_moog_sub37", "PRIMARY_ACOUSTIC_INSTRUMENT"),
        ("art_stephanbodzin_art", "gear_moog_sub37", "PRIMARY_ACOUSTIC_INSTRUMENT"),
        # Aphex Twin
        ("art_aphex", "gear_tb303", "PRIMARY_ACOUSTIC_INSTRUMENT"),
        ("art_aphex", "gear_tr808", "STUDIO_HARDWARE_SYNTH"),
        ("art_aphextwin", "gear_tb303", "PRIMARY_ACOUSTIC_INSTRUMENT"),
        ("art_aphextwin", "gear_tr808", "STUDIO_HARDWARE_SYNTH"),
        # BICEP
        ("art_bicep", "gear_tb303", "STUDIO_HARDWARE_SYNTH"),
        ("art_bicep", "gear_tr909", "STUDIO_HARDWARE_SYNTH"),
        # Tycho
        ("art_tycho", "gear_prophet6", "PRIMARY_ACOUSTIC_INSTRUMENT"),
        ("art_tycho", "gear_moog_sub37", "STUDIO_HARDWARE_SYNTH"),
        # Studios
        ("std_hansa", "gear_ssl4000", "INSTALLED_STUDIO_GEAR"),
        ("std_hansa", "gear_studer_a800", "INSTALLED_STUDIO_GEAR"),
        ("std_abbeyroad", "gear_neve8078", "INSTALLED_STUDIO_GEAR"),
        ("std_abbeyroad", "gear_studer_a800", "INSTALLED_STUDIO_GEAR"),
        ("std_sunsetsound", "gear_ssl4000", "INSTALLED_STUDIO_GEAR"),
        ("std_electriclady", "gear_neve8078", "INSTALLED_STUDIO_GEAR"),
        # Venues
        ("ven_berghain", "gear_funktion_one", "ACOUSTIC_SYSTEM_INSTALLED"),
        ("ven_tresor", "gear_funktion_one", "ACOUSTIC_SYSTEM_INSTALLED"),
        ("ven_warung", "gear_funktion_one", "ACOUSTIC_SYSTEM_INSTALLED"),
        ("ven_revolver", "gear_funktion_one", "ACOUSTIC_SYSTEM_INSTALLED"),
        ("ven_fabric", "gear_dnb_soundscape", "ACOUSTIC_SYSTEM_INSTALLED"),
    ]

    def enrich_density(self, industry_graph: MusicIndustryGraph) -> Dict[str, Any]:
        """Inject inclusion closures, hardware nodes, and triadic relationships."""
        graph = industry_graph.graph
        stats = {
            "hardware_nodes_added": 0,
            "hardware_edges_added": 0,
            "shared_studio_edges_added": 0,
            "label_mate_edges_added": 0,
            "sound_system_edges_added": 0,
            "corridor_peer_edges_added": 0,
            "genre_hybrid_edges_added": 0,
        }

        # 1. Ingest Hardware Gear & Sound System Nodes
        for gid, gname, gcat, gsig in self.HARDWARE_GEAR_CORPUS:
            if gid not in graph:
                gear_ent = BaseEntity(
                    id=gid,
                    name=gname,
                    entity_type=EntityType.TRACK,  # Subsumed under infrastructure schema
                    attributes={
                        "category": "Studio Hardware & Acoustics",
                        "gear_type": gcat,
                        "acoustic_signature": gsig,
                    },
                )
                industry_graph.add_entity(gear_ent)
                stats["hardware_nodes_added"] += 1

        # Link Entities to Hardware Gear
        for src, dst, rel in self.GEAR_USAGE_MAP:
            if src in graph and dst in graph:
                if not graph.has_edge(src, dst):
                    graph.add_edge(
                        src,
                        dst,
                        rel_type=rel,
                        weight=0.95,
                        is_current=True,
                        metadata={"type": "hardware_acoustic_link"},
                    )
                    stats["hardware_edges_added"] += 1

        # 2. Triadic Inclusion: Shared Studio Acoustic Space (SHARED_STUDIO_ACOUSTICS)
        studio_to_artists = defaultdict(list)
        for u, v, d in graph.edges(data=True):
            if d.get("rel_type") == "RECORDED_AT":
                studio_to_artists[v].append(u)

        for std_id, artists in studio_to_artists.items():
            unique_artists = list(set(artists))
            for i in range(len(unique_artists)):
                for j in range(i + 1, len(unique_artists)):
                    a1, a2 = unique_artists[i], unique_artists[j]
                    if not graph.has_edge(a1, a2):
                        graph.add_edge(
                            a1,
                            a2,
                            rel_type="SHARED_STUDIO_ACOUSTICS",
                            weight=0.88,
                            shared_studio=std_id,
                            metadata={"inclusion_type": "triadic_studio_closure"},
                        )
                        stats["shared_studio_edges_added"] += 1

        # 3. Triadic Inclusion: Label Roster Fellowship (LABEL_MATE_OF)
        label_to_artists = defaultdict(list)
        for u, v, d in graph.edges(data=True):
            if d.get("rel_type") == "SIGNED_TO":
                label_to_artists[v].append(u)

        for lbl_id, artists in label_to_artists.items():
            unique_artists = list(set(artists))
            for i in range(len(unique_artists)):
                for j in range(i + 1, len(unique_artists)):
                    a1, a2 = unique_artists[i], unique_artists[j]
                    if not graph.has_edge(a1, a2):
                        graph.add_edge(
                            a1,
                            a2,
                            rel_type="LABEL_MATE_OF",
                            weight=0.85,
                            shared_label=lbl_id,
                            metadata={"inclusion_type": "triadic_label_closure"},
                        )
                        stats["label_mate_edges_added"] += 1

        # 4. Sound System Affinity Closures (MATCHES_SOUND_SYSTEM_FIDELITY)
        gear_to_entities = defaultdict(list)
        for u, v, d in graph.edges(data=True):
            if "ACOUSTIC_SYSTEM_INSTALLED" in d.get("rel_type", "") or "PRIMARY_ACOUSTIC" in d.get("rel_type", ""):
                gear_to_entities[v].append(u)

        for gid, ents in gear_to_entities.items():
            unique_ents = list(set(ents))
            for i in range(len(unique_ents)):
                for j in range(i + 1, len(unique_ents)):
                    e1, e2 = unique_ents[i], unique_ents[j]
                    if not graph.has_edge(e1, e2):
                        graph.add_edge(
                            e1,
                            e2,
                            rel_type="MATCHES_SOUND_SYSTEM_FIDELITY",
                            weight=0.90,
                            sound_system=gid,
                            metadata={"inclusion_type": "hardware_sound_affinity"},
                        )
                        stats["sound_system_edges_added"] += 1

        # 5. Inter-City Corridor Clustering & Scene Peer Inclusions (CORRIDOR_SCENE_PEER)
        city_to_nodes = defaultdict(list)
        for u, v, d in graph.edges(data=True):
            rel = d.get("rel_type", "")
            if rel in ["BASED_IN_CITY", "OPERATES_IN_CITY", "HOSTED_IN_CITY"]:
                city_to_nodes[v].append(u)

        for city_id, nodes in city_to_nodes.items():
            unique_nodes = list(set(nodes))
            for i in range(len(unique_nodes)):
                for j in range(i + 1, min(len(unique_nodes), i + 6)):
                    n1, n2 = unique_nodes[i], unique_nodes[j]
                    if not graph.has_edge(n1, n2):
                        graph.add_edge(
                            n1,
                            n2,
                            rel_type="CORRIDOR_SCENE_PEER",
                            weight=0.82,
                            city_hub=city_id,
                            metadata={"inclusion_type": "city_ecosystem_clustering"},
                        )
                        stats["corridor_peer_edges_added"] += 1

        # 6. Cross-Genre Ancestral Influences & Micro-Genre Inclusions
        genre_influences = [
            ("tax_techno", "tax_house", "HISTORICAL_CROSS_POLLINATION", 0.92),
            ("tax_industrial_techno", "tax_melodic_techno", "CONTEMPORARY_DIALECTIC", 0.88),
            ("tax_krautrock_synth", "tax_ambient", "ANCESTRAL_TIMBRE_INFLUENCE", 0.95),
            ("tax_afrobeats", "tax_house", "RHYTHMIC_FUSION_CORRIDOR", 0.94),
            ("tax_reggae_dub", "tax_trip_hop", "DUB_SOUNDSYSTEM_LINEAGE", 0.98),
            ("tax_reggae_dub", "tax_drum_and_bass", "JUNGLE_BREAKBEAT_ROOT", 0.97),
            ("tax_post_minimalism", "tax_ambient", "ACOUSTIC_REVERBERATION_LINE", 0.96),
        ]
        for g1, g2, rel, w in genre_influences:
            if g1 in graph and g2 in graph:
                if not graph.has_edge(g1, g2):
                    graph.add_edge(
                        g1,
                        g2,
                        rel_type=rel,
                        weight=w,
                        metadata={"inclusion_type": "genre_genealogy"},
                    )
                    stats["genre_hybrid_edges_added"] += 1

        total_injected = sum(stats.values())
        logger.info(
            "Graph Density Inclusion Complete: %d new inclusion edges across %d hardware nodes (Total Graph: %d nodes, %d edges).",
            total_injected - stats["hardware_nodes_added"],
            stats["hardware_nodes_added"],
            len(graph.nodes),
            len(graph.edges),
        )

        return {
            "density_stats": stats,
            "total_nodes": len(graph.nodes),
            "total_edges": len(graph.edges),
            "graph_density": round(
                (2.0 * len(graph.edges)) / (len(graph.nodes) * (len(graph.nodes) - 1)),
                5,
            )
            if len(graph.nodes) > 1
            else 0.0,
        }
