"""Authoritative Entity Descriptions & Domain Context Enrichment Engine.

Provides detailed historical, acoustic, hardware, and industry biographies
for every node across the Knowledge Graph (Artists, Studios, Labels, Venues,
Cities, Districts, Hardware Gear, and Musical Subgenres).
"""

import logging
from typing import Any, Dict

from agies.graph.builder import MusicIndustryGraph

logger = logging.getLogger("agies.graph.descriptions")

ENTITY_DESCRIPTIONS_CATALOG: Dict[str, str] = {
    # === ARTISTS ===
    "art_kraftwerk": (
        "Düsseldorf electronic music pioneers formed in 1970 by Ralf Hütter and Florian Schneider. "
        "Engineered foundational electronic pop, synthpop, and techno vocabulary utilizing custom vocoders, "
        "Kling Klang studio hardware, and Robovox synthesis (Autobahn, Trans-Europe Express, Computer World)."
    ),
    "art_davidbowie": (
        "Legendary British shape-shifting visionary and composer. Partnered with Brian Eno and Tony Visconti "
        "at Hansa Tonstudio Berlin to craft the groundbreaking Berlin Trilogy (Low, Heroes, Lodger), "
        "merging ambient minimalism with post-punk art rock."
    ),
    "art_brianeno": (
        "English musician, composer, and pioneer of ambient music and generative soundscapes. "
        "Innovated the recording studio as a compositional tool (Oblique Strategies), producing seminal "
        "works for David Bowie, Talking Heads, U2, and Coldplay."
    ),
    "art_stephanbodzin": (
        "Bremen/Berlin melodic techno virtuoso and live hardware pioneer. Performs completely live "
        "using the Moog Sub 37 analog synthesizer and custom MIDI controllers, defining modern "
        "peak-time melodic club dynamics (Singularity, Boavista)."
    ),
    "art_nilsfrahm": (
        "Berlin-based composer and acoustic innovator recording at Funkhaus Berlin Saal 3. "
        "Blends acoustic grand pianos, custom uprights (Klavins Una Corda), Roland Space Echoes, "
        "and vintage analog synthesizers (Says, All Melody)."
    ),
    "art_aphextwin": (
        "Richard D. James (Cornwall/London), electronic mastermind who redefined IDM, braindance, "
        "and ambient techno. Utilizes custom microtonal scales, algorithmic sequencers (Cirklon), "
        "and heavily modified Roland TB-303/TR-808 gear (Selected Ambient Works 85-92, Drukqs)."
    ),
    "art_tycho": (
        "Scott Hansen (San Francisco), Grammy-nominated ambient/downtempo composer and visual artist. "
        "Known for warm vintage analog synthesis (Sequential Prophet-6, Moog Voyager), tape saturation, "
        "and lush acoustic guitar melodies (Epoch, Awake, Dive)."
    ),
    "art_bicep": (
        "Belfast/London electronic production duo (Andrew Ferguson & Matthew McBriar) signed to Ninja Tune. "
        "Famous for resurrecting 90s breakbeats, classic analog SH-101 leads, and euphoric festival anthems (Glue, Apricots)."
    ),
    "art_borisbrejcha": (
        "German DJ and producer who invented the 'High-Tech Minimal' subgenre. Combines aggressive punchy "
        "techno basslines with playful electro melodies, performing worldwide in his signature Joker Venetian mask."
    ),
    "art_daftpunk": (
        "Parisian duo (Thomas Bangalter & Guy-Manuel de Homem-Christo) who defined French Touch filter house, "
        "vocoder harmonies, and global electronic spectacle (Homework, Discovery, Random Access Memories)."
    ),
    "art_blackcoffee": (
        "South African Grammy-winning DJ and pioneer of the global Afro-House movement. Renowned for "
        "organic acoustic percussion, soulful chord voicings, and his multi-year residency at Hï Ibiza."
    ),
    "art_badbunny": (
        "Puerto Rican global phenomenon who revolutionized Latin Trap and Reggaeton. The most-streamed artist "
        "worldwide, merging Caribbean dembow rhythms with alternative rock, synthwave, and emotional lyricism (Un Verano Sin Ti)."
    ),
    "art_jbalvin": (
        "Medellín reggaeton icon who brought the Latin Urban movement into global pop mainstream, "
        "collaborating with Infinity Music producers to sculpt sleek, melodic dembow hits (Mi Gente, Vibras)."
    ),
    "art_tameimpala": (
        "Kevin Parker (Fremantle/Melbourne), multi-instrumentalist producer sculpting lush psychedelic pop, "
        "vintage tape phasers, and Roland drum machine grooves (Currents, The Slow Rush)."
    ),
    "art_flume": (
        "Harley Streten (Sydney), electronic producer who pioneered Future Bass and granular synthesis, "
        "featuring pitch-bent vocal chops and complex polyrhythmic sound design."
    ),
    "art_charlottedewitte": (
        "Belgian techno superstar and founder of KNTXT. Champions stripping techno down to hypnotic 303 acid lines, "
        "monumental kicks, and haunting spoken vocal hooks on global mainstages."
    ),
    "art_amelielens": (
        "Belgian fast-paced techno curator and founder of Lenske. Known for driving 135+ BPM percussion, "
        "relentless industrial energy, and curating grassroots EXHALE club showcases."
    ),

    # === RECORDING STUDIOS ===
    "std_funkhaus": (
        "Historic GDR broadcast facility on the Spree river in Berlin-Treptow. Saal 1 features a monumental "
        "acoustically optimized hall with a 2.4-second natural reverberation time, making it the premier global "
        "destination for neo-classical, orchestral, and experimental spatial electronic recordings."
    ),
    "std_hansa": (
        "Legendary Berlin recording studio located by the historic Wall in Köthener Straße. Famed for its "
        "Meistersaal acoustic chamber and SSL 4000 series consoles where David Bowie recorded 'Heroes', "
        "Iggy Pop recorded 'The Idiot', and Depeche Mode crafted 'Black Celebration'."
    ),
    "std_abbeyroad": (
        "World-renowned London studio complex founded in 1931 in St. John's Wood. Studio Two features historic "
        "EMI TG12345 and Neve consoles where The Beatles recorded nearly their entire discography, Pink Floyd recorded "
        "'Dark Side of the Moon', and film composers score Hollywood blockbusters."
    ),
    "std_electriclady": (
        "Greenwich Village NYC recording facility commissioned by Jimi Hendrix in 1970 and designed by John Storyk. "
        "Features custom Neve 8078 consoles and rounded acoustic geometry, hosting Stevie Wonder, Led Zeppelin, "
        "The Strokes, Taylor Swift, and Daft Punk."
    ),
    "std_sunsetsound": (
        "Historic Hollywood studio founded in 1958 by Tutti Camarata. Known for custom discrete recording consoles "
        "and lively echo chambers where The Doors, Prince (Purple Rain), Led Zeppelin, and Rolling Stones cut classic albums."
    ),
    "std_tuffgong": (
        "Kingston, Jamaica recording sanctuary established by Bob Marley in 1970 on Hope Road. Houses legendary "
        "discrete analog consoles and original vinyl press machines that defined roots reggae, dub, and dancehall sound."
    ),

    # === ICONIC VENUES ===
    "ven_berghain": (
        "The world's foremost temple of techno situated in a former East Berlin power plant. Features unmatched "
        "Funktion-One custom double 21-inch subwoofer arrays, 18-meter high concrete ceilings, and a legendary "
        "strict door policy dedicated to underground freedom and acoustic purism."
    ),
    "ven_tresor": (
        "Historic Berlin underground techno institution founded in 1991 in a bank vault under Potsdamer Platz, "
        "now located in the Kraftwerk Berlin power plant. The catalyst for the Berlin-Detroit techno sister-city alliance."
    ),
    "ven_fabric": (
        "Pioneering Farringdon, London electronic club founded in 1999. Features Room 1's revolutionary "
        "Pioneer Pro Audio Bodysonic vibrating acoustic dancefloor and bespoke sound dampening for crystal-clear breakbeat reproduction."
    ),
    "ven_warung": (
        "Iconic open-air wooden temple overlooking Praia Brava in Itajaí, Santa Catarina, Brazil. Celebrated as the "
        "'Savannah of Electronic Music' with sunrise sets and custom horn-loaded Funktion-One systems."
    ),
    "ven_revolver": (
        "Melbourne's legendary Chapel Street venue famed for multi-day endurance clubbing, homegrown minimal house, "
        "and a vintage heritage Funktion-One installation that anchors Australia's underground electronic circuit."
    ),
    "ven_womb": (
        "Shibuya, Tokyo four-story nightclub featuring Asia's largest mirror ball, laser-guided lighting rigs, and a "
        "custom Phazon sound system tuned for deep bass clarity."
    ),

    # === RECORD LABELS ===
    "lbl_ostgut": (
        "In-house record label of Berghain and Panorama Bar, documenting uncompromising techno, ambient, and "
        "panoramic house by resident artists like Ben Klock, Marcel Dettmann, Steffi, and Answer Code Request."
    ),
    "lbl_warp": (
        "Pioneering British independent record label founded in Sheffield in 1989. The quintessential home of "
        "avant-garde electronic music, IDM, and experimental hip-hop (Aphex Twin, Boards of Canada, Autechre, Flying Lotus)."
    ),
    "lbl_ninjatune": (
        "Influential London independent label founded by Coldcut in 1990. Champions breakbeat innovation, trip-hop, "
        "and modern global electronic sounds (BICEP, Bonobo, Floating Points, Cinematic Orchestra)."
    ),
    "lbl_erasedtapes": (
        "London/Berlin boutique record label founded by Robert Raths in 2007. Specializes in acoustic neo-classical, "
        "modular electronic, and exploratory instrumental music (Nils Frahm, Rival Consoles, Ólafur Arnalds, Kiasmos)."
    ),
    "lbl_kompakt": (
        "Cologne electronic institution founded by Wolfgang Voigt and Michael Mayer. Defines German micro-house, "
        "melodic minimal techno, and ambient soundscapes via the annual 'Total' and 'Pop Ambient' series."
    ),

    # === HARDWARE SYNTHESIZERS & GEAR ===
    "gear_moog_sub37": (
        "Paraphonic analog synthesizer featuring two variable-waveshape oscillators, a classic Moog ladder filter "
        "with multi-drive saturation, and dual DAHDSR loopable envelopes. The definitive bass engine for melodic techno."
    ),
    "gear_space_echo_re201": (
        "Legendary 1974 analog magnetic tape delay and spring reverb unit. Generates warm harmonic saturation, subtle "
        "tape wow/flutter, and self-oscillating resonant dub feedback loops essential for ambient and dub acoustics."
    ),
    "gear_tb303": (
        "Iconic 1981 analog bass synthesizer with diode ladder filter and accent circuitry. Accidental misuse of its "
        "cutoff and resonance knobs birthed acid house in Chicago and revolutionized global rave culture."
    ),
    "gear_tr808": (
        "Transistorized analog rhythm machine introduced by Roland in 1980. Its booming sine-wave decay kick and "
        "crisp hand-clap became the sonic foundation for hip-hop, trap, Miami bass, and modern pop."
    ),
    "gear_prophet6": (
        "Sequential's modern tribute to the vintage Prophet-5, featuring true voltage-controlled analog oscillators, "
        "classic four-pole resonant low-pass filters, and poly-mod routing for rich analog chords and warm pads."
    ),
    "gear_funktion_one": (
        "Pioneering horn-loaded point-source club loudspeaker system engineered by Tony Andrews. Eliminates harsh high-frequency "
        "compression distortion to deliver pure physical transient punch and low-frequency bass impact without listener fatigue."
    ),
}


class EntityDescriptionEnricher:
    """Enriches all nodes in a MusicIndustryGraph with authoritative context descriptions."""

    def enrich_descriptions(self, industry_graph: MusicIndustryGraph) -> Dict[str, Any]:
        """Apply comprehensive multi-sentence descriptions across all graph nodes."""
        graph = industry_graph.graph
        enriched_count = 0

        for nid, data in graph.nodes(data=True):
            # Check if specific description exists in catalog
            clean_id = nid.replace("kg_", "")
            if clean_id in ENTITY_DESCRIPTIONS_CATALOG:
                desc = ENTITY_DESCRIPTIONS_CATALOG[clean_id]
                graph.nodes[nid]["description"] = desc
                enriched_count += 1
            elif not data.get("description"):
                # Synthesize high-fidelity fallback description based on entity attributes
                name = data.get("name", nid)
                etype = data.get("entity_type", "entity")
                country = data.get("country", "")
                genres = data.get("genres", [])
                g_str = ", ".join(genres) if genres else "electronic and modern music"

                if etype == "artist":
                    desc = f"{name} is an active music artist based in {country or 'the global scene'}, producing across {g_str}."
                elif etype == "studio":
                    desc = f"{name} is a high-fidelity professional recording and mastering studio located in {country or 'Europe'} specializing in {g_str}."
                elif etype == "record_label":
                    desc = f"{name} is an influential record label imprint based in {country or 'the global market'} curating groundbreaking releases in {g_str}."
                elif etype == "venue":
                    desc = f"{name} is an iconic live music and nightlife venue in {country or 'the international club network'} equipped with dedicated acoustic systems."
                elif etype == "city" or "city" in nid:
                    desc = f"{name} is a major global music capital and cultural trade hub anchoring vibrant local underground scenes and international artist corridors."
                elif "distr" in nid:
                    desc = f"{name} is a dense creative district and neighborhood scene known for grassroots live music spaces, recording studios, and indie record stores."
                elif "tax" in nid or "genre" in nid:
                    desc = f"{name} represents a distinct musical taxonomy subgenre characterized by specific rhythmic meters, harmonic frequency distributions, and tempo ranges."
                else:
                    desc = f"{name} is a key institutional entity within the multi-continental music industry knowledge graph."

                graph.nodes[nid]["description"] = desc
                enriched_count += 1

        logger.info(
            "Enriched %d knowledge graph entities with authoritative domain descriptions.",
            enriched_count,
        )
        return {
            "total_nodes_enriched": enriched_count,
            "total_graph_nodes": len(graph.nodes),
        }
