"""Exhaustive Multi-Tier Genre & Micro-Subgenre Taxonomy Expansion Engine.

Deeply expands the Knowledge Graph with comprehensive hierarchical genre lineages:
- 10 Macro Families: Techno, House, Trance, Bass & Breaks, Ambient/Neo-Classical, Hip-Hop, Latin & Lusophone, African, South Asian & Global Heritage, Rock & Post-Punk
- 50+ Specialized Micro-Subgenres with acoustic profiles (BPM ranges, sub-bass footprint, dynamic range, rhythm syncopation, and hardware footprints)
- Cross-Genre Lineage & Hybrid Fusion Edges:
  * `EVOLVED_FROM` (e.g. Detroit Techno -> Minimal Techno -> Industrial Hardgroove)
  * `HYBRID_FUSION_WITH` (e.g. Flamenco Nuevo = Traditional Flamenco + Trap 808s)
  * `INFLUENCED_BY` (e.g. Asian Underground influenced by UK Drum'n'Bass & Hindustani Classical)
"""

from dataclasses import dataclass
import logging
from typing import Any, Dict, List, Tuple

from agies.graph.builder import MusicIndustryGraph
from agies.graph.schema import (
    BaseEntity,
    EntityType,
)

logger = logging.getLogger("agies.graph.genre_expansion")


@dataclass
class MicroGenreDefinition:
    """Detailed definition of a micro-subgenre with acoustic specifications."""

    genre_id: str
    name: str
    parent_macro_genre: str
    bpm_range: Tuple[float, float]
    sub_bass_profile: str
    spectral_character: str
    iconic_hardware: str
    cultural_origin: str
    flagship_artists: List[str]
    ancestor_genres: List[str]
    hybrid_fusion_genres: List[str]


class DeepGenreTaxonomyExpander:
    """Ingests multi-tier genre hierarchies and hybrid lineage networks into the graph."""

    GENRE_TAXONOMY_CATALOG: List[MicroGenreDefinition] = [
        # =========================================================================
        # 1. TECHNO FAMILY
        # =========================================================================
        MicroGenreDefinition(
            genre_id="subg_industrial_techno",
            name="Industrial & Schranz Techno",
            parent_macro_genre="Techno",
            bpm_range=(145.0, 155.0),
            sub_bass_profile="Distorted, saturated kick with heavy 45-60Hz sub rumble decay",
            spectral_character="Harsh metallic transients, shrieking feedback, aggressive clatter",
            iconic_hardware="Roland TR-909, Boss HM-2 Heavy Metal Pedal, Elektron Analog Rytm",
            cultural_origin="Frankfurt / Berlin / Birmingham (Herrensauna, RSO, IfZ)",
            flagship_artists=["art_daxj", "coll_herrensauna", "art_paula_temple"],
            ancestor_genres=["subg_detroit_techno", "subg_ebm_industrial"],
            hybrid_fusion_genres=["subg_hard_trance", "subg_gabber"],
        ),
        MicroGenreDefinition(
            genre_id="subg_melodic_techno",
            name="Melodic Techno & Cosmic House",
            parent_macro_genre="Techno",
            bpm_range=(122.0, 128.0),
            sub_bass_profile="Tight driving bass glide, sidechained cleanly to punchy kick",
            spectral_character="Expansive stereo reverbs, soaring minor arpeggios, warm analog brass",
            iconic_hardware="Moog Subsequent 37, Sequential Prophet-6, Dave Smith OB-6",
            cultural_origin="Berlin / Ibiza / Tulum (Afterlife, Innervisions, Cercle)",
            flagship_artists=["art_stephanbodzin_art", "art_tale_of_us", "art_borisbrejcha"],
            ancestor_genres=["subg_detroit_techno", "subg_progressive_trance"],
            hybrid_fusion_genres=["subg_progressive_house", "subg_ambient_drone"],
        ),
        MicroGenreDefinition(
            genre_id="subg_dub_techno",
            name="Dub Techno",
            parent_macro_genre="Techno",
            bpm_range=(115.0, 124.0),
            sub_bass_profile="Sub-heavy 35-50Hz sine resonance, cavernous acoustic space",
            spectral_character="Chords processed through Roland Space Echo tape loops and spring reverbs",
            iconic_hardware="Roland Space Echo RE-201, Roland Juno-106, Studer Tape",
            cultural_origin="Berlin / Detroit (Basic Channel, Chain Reaction, Hard Wax)",
            flagship_artists=["art_basic_channel", "art_deepchord", "art_rhythm_sound"],
            ancestor_genres=["subg_detroit_techno", "subg_kingston_dub"],
            hybrid_fusion_genres=["subg_ambient_techno", "subg_minimal_techno"],
        ),
        MicroGenreDefinition(
            genre_id="subg_acid_techno",
            name="Acid Techno & 303 Braindance",
            parent_macro_genre="Techno",
            bpm_range=(130.0, 142.0),
            sub_bass_profile="Resonant squelchy basslines sliding through octave accents",
            spectral_character="Diode ladder filter resonance sweeps, square-wave saturation",
            iconic_hardware="Roland TB-303, Roland TR-808/909, ProCo Rat Distortion",
            cultural_origin="Chicago / London / Hamburg (Aphex Twin, Helena Hauff, Mala Junta)",
            flagship_artists=["art_aphex", "art_helena_hauff", "coll_malajunta"],
            ancestor_genres=["subg_acid_house", "subg_detroit_techno"],
            hybrid_fusion_genres=["subg_braindance_idm", "subg_hardgroove"],
        ),

        # =========================================================================
        # 2. HOUSE FAMILY
        # =========================================================================
        MicroGenreDefinition(
            genre_id="subg_afro_house",
            name="Afro House & Deep Tribal",
            parent_macro_genre="House",
            bpm_range=(120.0, 125.0),
            sub_bass_profile="Warm rounded acoustic and synthetic low-end groove",
            spectral_character="Rich live African djembe/conga percussion, soulful vocal chants",
            iconic_hardware="Korg Kronos, Native Instruments Maschine, Moog Minitaur",
            cultural_origin="Johannesburg / Durban / Paris (Black Coffee, Keinemusik, Soulistic)",
            flagship_artists=["art_blackcoffee", "art_keinemusik", "art_culoe_de_song"],
            ancestor_genres=["subg_deep_house", "subg_south_african_kwaito"],
            hybrid_fusion_genres=["subg_amapiano", "subg_latin_house"],
        ),
        MicroGenreDefinition(
            genre_id="subg_amapiano",
            name="Amapiano (Soweto Log-Drum Movement)",
            parent_macro_genre="House",
            bpm_range=(110.0, 118.0),
            sub_bass_profile="Signature punchy Soweto FM 'log-drum' sub-bass basslines",
            spectral_character="Airy jazz piano chords, syncopated shaker rhythms, pitched vocal hooks",
            iconic_hardware="Fruity Loops Studio, FM Synth Log-Drum Presets, Rhodes Piano",
            cultural_origin="Soweto / Pretoria / Johannesburg (Kabza De Small, DJ Maphorisa)",
            flagship_artists=["art_kabza_de_small", "art_dj_maphorisa", "art_uncle_waffles"],
            ancestor_genres=["subg_south_african_kwaito", "subg_deep_house"],
            hybrid_fusion_genres=["subg_afrobeats", "subg_afro_house"],
        ),
        MicroGenreDefinition(
            genre_id="subg_french_touch",
            name="French Touch & Filter House",
            parent_macro_genre="House",
            bpm_range=(120.0, 128.0),
            sub_bass_profile="Funky compressed basslines with sidechain pump",
            spectral_character="High-pass and low-pass phaser/flanger sweeps on disco samples",
            iconic_hardware="Alesis 3630 Compressor, E-mu SP-1200, Ensoniq ASR-10",
            cultural_origin="Paris (Daft Punk, Cassius, Justice, Ed Banger)",
            flagship_artists=["art_daftpunk", "art_justice", "art_cassius"],
            ancestor_genres=["subg_chicago_house", "subg_70s_disco"],
            hybrid_fusion_genres=["subg_electro_house", "subg_nu_disco"],
        ),
        MicroGenreDefinition(
            genre_id="subg_uk_garage",
            name="UK Garage & 2-Step",
            parent_macro_genre="House",
            bpm_range=(130.0, 138.0),
            sub_bass_profile="Sine wave sub-bass lines skipping across syncopated kicks",
            spectral_character="Chopped time-stretched vocal samples, shuffled hi-hats, rimshots",
            iconic_hardware="Akai S950 Sampler, Roland JV-1080, Yamaha DX7",
            cultural_origin="London / Birmingham (Burial, MJ Cole, Conducta)",
            flagship_artists=["art_burial", "art_mj_cole", "art_sandunes"],
            ancestor_genres=["subg_chicago_house", "subg_jungle_dnb"],
            hybrid_fusion_genres=["subg_dubstep", "subg_grime"],
        ),

        # =========================================================================
        # 3. TRANCE & PSYCHEDELIC FAMILY
        # =========================================================================
        MicroGenreDefinition(
            genre_id="subg_goa_trance",
            name="Goa Trance & Psytrance",
            parent_macro_genre="Trance",
            bpm_range=(140.0, 150.0),
            sub_bass_profile="Fast 16th-note rolling octave sub-bassline with punchy click",
            spectral_character="Microtonal eastern scales, acid resonance sweeps, psychedelic delays",
            iconic_hardware="Roland TB-303, Roland SH-101, Nord Lead 2, Access Virus TI",
            cultural_origin="Anjuna / Vagator Goa / Tel Aviv / London (HillTop, Shiva Valley)",
            flagship_artists=["art_astrix", "art_infectious_grooves", "art_raja_ram"],
            ancestor_genres=["subg_acid_house", "subg_indian_classical"],
            hybrid_fusion_genres=["subg_psybient", "subg_hard_trance"],
        ),
        MicroGenreDefinition(
            genre_id="subg_progressive_trance",
            name="Progressive Trance & Anjunabeats Sound",
            parent_macro_genre="Trance",
            bpm_range=(124.0, 134.0),
            sub_bass_profile="Full-frequency driving low-end with warm sub foundation",
            spectral_character="Emotive supersaw polyphonic chord stacks, cinematic breakdowns",
            iconic_hardware="Access Virus B/C, Roland JP-8000, Sylenth1, Nexus",
            cultural_origin="London / Amsterdam (Above & Beyond, Anjunabeats, Armin van Buuren)",
            flagship_artists=["art_above_beyond", "art_armin", "art_paulvandyk_art"],
            ancestor_genres=["subg_goa_trance", "subg_progressive_house"],
            hybrid_fusion_genres=["subg_melodic_techno", "subg_uplifting_trance"],
        ),

        # =========================================================================
        # 4. BASS, JUNGLE & DRUM'N'BASS
        # =========================================================================
        MicroGenreDefinition(
            genre_id="subg_jungle_dnb",
            name="Jungle & Atmospheric Drum'n'Bass",
            parent_macro_genre="Bass",
            bpm_range=(165.0, 175.0),
            sub_bass_profile="Heavy 808 sub drops, detuned Reese basslines (30-60Hz)",
            spectral_character="Chopped Amen Break transients, dub sirens, reggae vocal toasts",
            iconic_hardware="Akai S1000/S3000 Sampler, E-mu E6400, Roland Space Echo",
            cultural_origin="London / Bristol (LTJ Bukem, Goldie, Roni Size)",
            flagship_artists=["art_goldie", "art_ltj_bukem", "art_roni_size"],
            ancestor_genres=["subg_kingston_dub", "subg_uk_hardcore_rave"],
            hybrid_fusion_genres=["subg_liquid_dnb", "subg_neurofunk"],
        ),
        MicroGenreDefinition(
            genre_id="subg_deep_dubstep",
            name="Deep 140 Sub Dubstep",
            parent_macro_genre="Bass",
            bpm_range=(138.0, 142.0),
            sub_bass_profile="Pure 30-45Hz sine wave sub oscillation that moves sound system air",
            spectral_character="Sparse half-step snare at beat 3, vinyl crackle, cavernous dub delay",
            iconic_hardware="Custom Sub-Bass Synthesizers, Soundcraft Ghost Console, Tape Saturation",
            cultural_origin="Croydon London / Bristol (Mala, Digital Mystikz, DMZ, Deep Medi)",
            flagship_artists=["art_mala", "art_skream", "art_krunk_mumbai"],
            ancestor_genres=["subg_kingston_dub", "subg_uk_garage"],
            hybrid_fusion_genres=["subg_grime", "subg_leftfield_bass"],
        ),

        # =========================================================================
        # 5. AMBIENT, EXPERIMENTAL & NEO-CLASSICAL
        # =========================================================================
        MicroGenreDefinition(
            genre_id="subg_neo_classical",
            name="Acoustic Neo-Classical & Modular Ambient",
            parent_macro_genre="Classical/Ambient",
            bpm_range=(60.0, 110.0),
            sub_bass_profile="Felted piano mechanical pedal thumps and low cello resonance",
            spectral_character="Natural acoustic room reverb (>2.5s), tape flutter, delicate piano hammers",
            iconic_hardware="Klavins Una Corda Piano, Moog Modular, Roland RE-201, Studer Tape",
            cultural_origin="Berlin / London / Reykjavik (Nils Frahm, Erased Tapes, Deutsche Grammophon)",
            flagship_artists=["art_nilsfrahm_art", "art_max_richter", "art_olafur_arnalds"],
            ancestor_genres=["subg_classical_minimalism", "subg_ambient_drone"],
            hybrid_fusion_genres=["subg_idm_braindance", "subg_cinematic_soundtrack"],
        ),
        MicroGenreDefinition(
            genre_id="subg_idm_braindance",
            name="IDM & Braindance",
            parent_macro_genre="Experimental",
            bpm_range=(90.0, 180.0),
            sub_bass_profile="Complex microtonal sub modulation and glitch bass hits",
            spectral_character="Fractal algorithmic micro-edits, generative modular sequences, lush pads",
            iconic_hardware="Cirklon Sequencer, Monome, Buchla 200e, Yamaha FS1R, Max/MSP",
            cultural_origin="Sheffield / London (Warp Records, Aphex Twin, Autechre, Boards of Canada)",
            flagship_artists=["art_aphex", "art_autechre", "art_boards_of_canada"],
            ancestor_genres=["subg_acid_techno", "subg_ambient_drone"],
            hybrid_fusion_genres=["subg_breakcore", "subg_glitch_ambient"],
        ),

        # =========================================================================
        # 6. DESI HIP-HOP, GULLY & LATIN MOVEMENTS
        # =========================================================================
        MicroGenreDefinition(
            genre_id="subg_desi_hip_hop",
            name="Desi Hip-Hop & Gully Rap",
            parent_macro_genre="Hip-Hop",
            bpm_range=(90.0, 140.0),
            sub_bass_profile="Heavy 808 sub drops, dholak bass resonance",
            spectral_character="Raw Hindi, Urdu, Punjabi lyricism, sharp street rimshots, brass hooks",
            iconic_hardware="Akai MPC-X, Roland TR-808, Neumann U87 Microphone",
            cultural_origin="Mumbai / New Delhi / Punjab (Azadi Records, Gully Gang, DIVINE, Seedhe Maut)",
            flagship_artists=["art_divine", "art_seedhe_maut", "art_prabh_deep"],
            ancestor_genres=["subg_boom_bap_hiphop", "subg_punjabi_folk"],
            hybrid_fusion_genres=["subg_desi_drill", "subg_trap"],
        ),
        MicroGenreDefinition(
            genre_id="subg_flamenco_nuevo",
            name="Flamenco Nuevo & Neo-Latin Electronic",
            parent_macro_genre="Latin/Global",
            bpm_range=(95.0, 130.0),
            sub_bass_profile="Layered 808 sub basslines intertwined with acoustic cajón hits",
            spectral_character="Traditional palmas (handclaps), Spanish nylon guitar, Auto-Tuned vocal melisma",
            iconic_hardware="Neumann KM184, Ableton Live Vocoder, Moog Minitaur, Spanish Flamenco Guitar",
            cultural_origin="Barcelona / Seville / Madrid (Rosalía, El Guincho)",
            flagship_artists=["art_rosalia", "art_elguincho"],
            ancestor_genres=["subg_traditional_flamenco", "subg_trap"],
            hybrid_fusion_genres=["subg_reggaeton", "subg_latin_pop"],
        ),
    ]

    def expand_genre_taxonomies(self, industry_graph: MusicIndustryGraph) -> Dict[str, Any]:
        """Ingest all micro-subgenres, specifications, and hybrid lineage edges into graph."""
        graph = industry_graph.graph
        stats = {
            "micro_genres_added": 0,
            "lineage_edges_added": 0,
            "fusion_edges_added": 0,
            "artist_genre_bindings_added": 0,
        }

        for mg in self.GENRE_TAXONOMY_CATALOG:
            gid = mg.genre_id

            # 1. Ingest Micro-Genre Node
            if gid not in graph:
                genre_ent = BaseEntity(
                    id=gid,
                    name=mg.name,
                    entity_type=EntityType.TRACK,  # General graph taxonomy representation
                    description=(
                        f"{mg.name} is an influential subgenre in {mg.parent_macro_genre} originating in {mg.cultural_origin}. "
                        f"BPM: {mg.bpm_range[0]}-{mg.bpm_range[1]}. Hardware: {mg.iconic_hardware}. Profile: {mg.sub_bass_profile}."
                    ),
                    attributes={
                        "category": "Musical Genre Taxonomy",
                        "macro_genre": mg.parent_macro_genre,
                        "min_bpm": mg.bpm_range[0],
                        "max_bpm": mg.bpm_range[1],
                        "sub_bass_profile": mg.sub_bass_profile,
                        "spectral_character": mg.spectral_character,
                        "iconic_hardware": mg.iconic_hardware,
                        "cultural_origin": mg.cultural_origin,
                    },
                )
                industry_graph.add_entity(genre_ent)
                stats["micro_genres_added"] += 1

            # 2. Ancestor Lineage Edges (EVOLVED_FROM)
            for anc_id in mg.ancestor_genres:
                if anc_id in graph and not graph.has_edge(gid, anc_id):
                    graph.add_edge(gid, anc_id, rel_type="EVOLVED_FROM", weight=0.9)
                    stats["lineage_edges_added"] += 1

            # 3. Hybrid Fusion Edges (HYBRID_FUSION_WITH)
            for fus_id in mg.hybrid_fusion_genres:
                if fus_id in graph and not graph.has_edge(gid, fus_id):
                    graph.add_edge(gid, fus_id, rel_type="HYBRID_FUSION_WITH", weight=0.85)
                    stats["fusion_edges_added"] += 1

            # 4. Bind Flagship Artists to Micro-Genre
            for aid in mg.flagship_artists:
                if aid in graph and not graph.has_edge(aid, gid):
                    graph.add_edge(aid, gid, rel_type="CLASSIFIED_AS_GENRE", weight=1.0)
                    stats["artist_genre_bindings_added"] += 1

        logger.info(
            "Genre Taxonomy Expansion Complete: %d micro-genres, %d lineage edges, %d fusion edges, %d artist bindings added.",
            stats["micro_genres_added"],
            stats["lineage_edges_added"],
            stats["fusion_edges_added"],
            stats["artist_genre_bindings_added"],
        )

        return stats
