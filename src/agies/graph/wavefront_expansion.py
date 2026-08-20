"""Concentric Wave-Front Global Expansion Engine.

Slow-starts at Berlin grassroots underground anchor and progressively expands
radially outward wave-by-wave until the entire global electronic & acoustic music map is covered:

- Wave 0: Berlin Ground Zero (Mitte, Kreuzberg, Neukölln, Friedrichshain, Wedding, Lichtenberg, Schöneweide)
- Wave 1: Central European & German Neighbor Ring (Leipzig, Dresden, Hamburg, Prague, Warsaw, Cologne, Frankfurt, Munich)
- Wave 2: Western & Northern European Sister Hubs (Amsterdam, London, Paris, Brussels, Vienna, Copenhagen, Zurich)
- Wave 3: Mediterranean, Eastern & Caucasus Axis (Barcelona, Madrid, Milan, Rome, Tbilisi, Belgrade, Athens, Istanbul, Lisbon)
- Wave 4: Transatlantic & Global Megacities (New York, Detroit, Chicago, LA, São Paulo, Medellín, Tokyo, Seoul, Johannesburg, Melbourne)
"""

from dataclasses import dataclass
import logging
from typing import Any, Dict, List

from agies.graph.builder import MusicIndustryGraph
from agies.graph.schema import (
    BaseEntity,
    EntityType,
)

logger = logging.getLogger("agies.graph.wavefront_expansion")


@dataclass
class GeographicWaveCity:
    """City node and grassroots infrastructure inside a concentric geographic wave."""

    city_id: str
    city_name: str
    country: str
    wave_tier: int  # 0 to 4
    hub_type: str  # Underground Bastion, Global Sister Hub, etc.
    flagship_venues: List[Dict[str, str]]
    collectives: List[Dict[str, str]]
    record_stores: List[Dict[str, str]]
    connected_corridor_cities: List[str]
    acoustic_signature: str


class ConcentricGeographicWaveFrontExpander:
    """Manages radial outward wave-front expansion from Berlin across the globe."""

    WAVE_EXPANSION_CATALOG: List[GeographicWaveCity] = [
        # =========================================================================
        # WAVE 1: CENTRAL EUROPEAN & GERMAN NEIGHBOR RING
        # =========================================================================
        GeographicWaveCity(
            city_id="city_leipzig",
            city_name="Leipzig",
            country="Germany",
            wave_tier=1,
            hub_type="Underground Industrial Bastion",
            flagship_venues=[
                {"id": "ven_ifz_leipzig", "name": "Institut für Zukunft (IfZ)", "sound": "Custom Point-Source Industrial Rig", "desc": "Famous leftfield and political underground club in an old slaughterhouse."},
                {"id": "ven_distillery_leipzig", "name": "Distillery Leipzig", "sound": "Classic House & Techno PA", "desc": "East Germany's oldest electronic music club (est. 1992)."},
                {"id": "ven_ut_connewitz", "name": "UT Connewitz", "sound": "Historic Acoustic Cinema Hall", "desc": "Oldest surviving cinema in Germany hosting post-rock and neo-classical concerts."},
            ],
            collectives=[
                {"id": "coll_spinnerei_leipzig", "name": "Spinnerei Artist Cooperative", "desc": "Massive former cotton mill turned contemporary arts and sound design hub."},
            ],
            record_stores=[
                {"id": "store_hhv_leipzig", "name": "HHV Leipzig", "desc": "Underground vinyl and beat culture record outlet."},
            ],
            connected_corridor_cities=["city_berlin", "city_dresden", "city_prague"],
            acoustic_signature="Raw hypnotic techno, broken beats, and modular industrial textures (135-142 BPM)",
        ),
        GeographicWaveCity(
            city_id="city_dresden",
            city_name="Dresden",
            country="Germany",
            wave_tier=1,
            hub_type="Elbe Underground Circuit",
            flagship_venues=[
                {"id": "ven_objekt_klein_a", "name": "Objekt Klein A", "sound": "KV2 Audio Acoustic Array", "desc": "Industrial warehouse club in Dresden Neustadt for community-driven techno."},
                {"id": "ven_sektor_evolution", "name": "Sektor Evolution", "sound": "High-Impact Festival PA", "desc": "Underground club dedicated to dark ambient, psy, and hard techno."},
            ],
            collectives=[
                {"id": "coll_dresden_modular", "name": "Dresden Modular Jam Crew", "desc": "Grassroots hardware synthesizer and patch-cable electronic community."},
            ],
            record_stores=[
                {"id": "store_fat_fenders", "name": "Fat Fenders Records", "desc": "Essential Dresden electronic vinyl store and community hub."},
            ],
            connected_corridor_cities=["city_berlin", "city_leipzig", "city_prague"],
            acoustic_signature="Dark modular synthesis, acid techno, and experimental bass (138-145 BPM)",
        ),
        GeographicWaveCity(
            city_id="city_hamburg",
            city_name="Hamburg",
            country="Germany",
            wave_tier=1,
            hub_type="Hanseatic Harbour & Acid Hub",
            flagship_venues=[
                {"id": "ven_pudel_hamburg", "name": "Golden Pudel Club", "sound": "Intimate Audiophile Fishmarket Sound", "desc": "Legendary harbour-side subcultural club on the Elbe; the epicenter of dial/pudel aesthetics (Helena Hauff)."},
                {"id": "ven_pal_hamburg", "name": "PAL Hamburg", "sound": "Funktion-One Precision Array", "desc": "Uncompromising minimal and dark techno warehouse by Karoviertel."},
                {"id": "ven_uebel_hamburg", "name": "Uebel & Gefährlich", "sound": "Flakturm IV Anti-Aircraft Bunker PA", "desc": "Iconic multi-level club housed in the giant WWII St. Pauli bunker."},
            ],
            collectives=[
                {"id": "coll_reeperbahn_arts", "name": "St. Pauli Underground Collective", "desc": "Grassroots live export, indie showcase, and selector community."},
            ],
            record_stores=[
                {"id": "store_smallville_hamburg", "name": "Smallville Records", "desc": "Julius Steinhoff's cult deep house record store and label imprint."},
            ],
            connected_corridor_cities=["city_berlin", "city_amsterdam", "city_cologne"],
            acoustic_signature="Electro-acid vinyl pressure, raw breakbeats, and dubby deep house (124-136 BPM)",
        ),
        GeographicWaveCity(
            city_id="city_prague",
            city_name="Prague",
            country="Czech Republic",
            wave_tier=1,
            hub_type="Bohemian Avant-Garde Vault",
            flagship_venues=[
                {"id": "ven_ankali_prague", "name": "Ankali", "sound": "Custom Audiophile Sub-Bass Horns", "desc": "Former soap factory in Vršovice; intimate darkroom sanctuary for queer and leftfield techno."},
                {"id": "ven_fuchs2_prague", "name": "Fuchs2", "sound": "Void Acoustics Soundfield", "desc": "Brutalist island pavilion on Štvanice hosting avant-club and deconstructed electronics."},
                {"id": "ven_cross_club", "name": "Cross Club Prague", "sound": "Kinetic Industrial Steampunk Array", "desc": "Multi-story kinetic sculpture DIY club hosting dub, breakcore, and d&b."},
            ],
            collectives=[
                {"id": "coll_lunchmeat_prague", "name": "Lunchmeat Festival Collective", "desc": "International festival platform for advanced electronic music and digital visual art."},
            ],
            record_stores=[
                {"id": "store_garage_store_prague", "name": "Garage Store Prague", "desc": "Vršovice vinyl dispensary and cassette label repository."},
            ],
            connected_corridor_cities=["city_berlin", "city_dresden", "city_vienna"],
            acoustic_signature="Deconstructed club, polyrhythmic ambient, and heavyweight sub-low (128-144 BPM)",
        ),
        GeographicWaveCity(
            city_id="city_warsaw",
            city_name="Warsaw",
            country="Poland",
            wave_tier=1,
            hub_type="Vistula Fast-Groove Hub",
            flagship_venues=[
                {"id": "ven_jasna1_warsaw", "name": "Jasna 1", "sound": "d&b audiotechnik Precision Rig", "desc": "Historic downtown bank vault turned multi-room sanctuary for Polish electronic music."},
                {"id": "ven_smolna_warsaw", "name": "Smolna", "sound": "KV2 Audio Redline Sub-System", "desc": "Underground brick maze near the national museum with strict no-photo policy."},
            ],
            collectives=[
                {"id": "coll_dunno_warsaw", "name": "Dunno Recordings Collective", "desc": "Avant-garde cassette label and experimental club selectors."},
            ],
            record_stores=[
                {"id": "store_sideone_warsaw", "name": "Side One Records", "desc": "Chmielna street vinyl institution supplying Warsaw's premier DJs for two decades."},
            ],
            connected_corridor_cities=["city_berlin", "city_prague", "city_kyiv"],
            acoustic_signature="Fast Polish techno groove, hypnotic syncopated percussion, and dark wave (140-146 BPM)",
        ),
        GeographicWaveCity(
            city_id="city_cologne",
            city_name="Cologne & Düsseldorf",
            country="Germany",
            wave_tier=1,
            hub_type="Rhineland Micro-House & Krautrock Heart",
            flagship_venues=[
                {"id": "ven_gewoelbe_cologne", "name": "Gewölbe", "sound": "Martin Audio Underground Array", "desc": "Vault club under Westbahnhof celebrated for audiophile clarity and underground house."},
                {"id": "ven_salon_des_amateurs", "name": "Salon des Amateurs (Düsseldorf)", "sound": "Rotary Hi-Fi Audiophile Rig", "desc": "Kunsthalle bar where Lena Willikens & Vladimir Ivkovic created modern cosmic chug."},
                {"id": "ven_bootshaus_cologne", "name": "Bootshaus", "sound": "Funktion-One XXL Stadium Array", "desc": "Global festival-scale shipyard venue ranking among the world's top club sound systems."},
            ],
            collectives=[
                {"id": "coll_kompakt_cologne", "name": "Kompakt Total Collective", "desc": "Wolfgang Voigt & Michael Mayer's minimal melodic techno institution."},
            ],
            record_stores=[
                {"id": "store_kompakt_shop", "name": "Kompakt Records Shop", "desc": "Werderstraße vinyl boutique, publishing house, and worldwide distributor."},
            ],
            connected_corridor_cities=["city_berlin", "city_amsterdam", "city_brussels", "city_frankfurt"],
            acoustic_signature="Minimal ambient techno, micro-house, and slow cosmic krautrock (110-126 BPM)",
        ),
        GeographicWaveCity(
            city_id="city_frankfurt",
            city_name="Frankfurt & Offenbach",
            country="Germany",
            wave_tier=1,
            hub_type="Main Sound & Robert Johnson Legacy",
            flagship_venues=[
                {"id": "ven_robert_johnson", "name": "Robert Johnson (Offenbach)", "sound": "Custom Martin Audio + Wooden Dancefloor Acoustic Float", "desc": "Ata Macias' legendary minimalist wooden cube on the Main river; pure audiophile nirvana."},
                {"id": "ven_tanzhaus_west", "name": "Tanzhaus West", "sound": "Funktion-One Warehouse System", "desc": "Former paint factory industrial ground for underground Frankfurt techno."},
            ],
            collectives=[
                {"id": "coll_live_at_rj", "name": "Live at Robert Johnson Collective", "desc": "Influential label and resident fellowship defining Frankfurt-Offenbach house."},
            ],
            record_stores=[
                {"id": "store_tactile_frankfurt", "name": "Tactile Record Store", "desc": "Audiophile vinyl hub for house, disco, and deep minimal."},
            ],
            connected_corridor_cities=["city_berlin", "city_cologne", "city_munich", "city_zurich"],
            acoustic_signature="Stripped-down groove, deep Chicago-influenced house, and melodic techno (122-128 BPM)",
        ),
        GeographicWaveCity(
            city_id="city_munich",
            city_name="Munich",
            country="Germany",
            wave_tier=1,
            hub_type="Bavarian Audiophile & Synth Outpost",
            flagship_venues=[
                {"id": "ven_blitz_munich", "name": "Blitz Club", "sound": "Custom VOID Acoustics Incubus Acoustic Array", "desc": "Acoustically treated sound temple at Deutsches Museum with 3D-sculpted acoustic paneling."},
                {"id": "ven_rote_sonne", "name": "Rote Sonne", "sound": "Funktion-One Dark Space", "desc": "Cult underground basement club founded by DJ Hell and Munich techno pioneers."},
            ],
            collectives=[
                {"id": "coll_blitz_music", "name": "Blitz Music / Ilian Tape Lineage", "desc": "Zenker Brothers & Skee Mask breakbeat techno sound lineage."},
            ],
            record_stores=[
                {"id": "store_public_possession", "name": "Public Possession", "desc": "Cult Munich boutique record store, label, and design atelier."},
            ],
            connected_corridor_cities=["city_berlin", "city_frankfurt", "city_vienna", "city_zurich"],
            acoustic_signature="Heavy breakbeat techno, ambient IDM, and pristine dynamic low-end (130-140 BPM)",
        ),

        # =========================================================================
        # WAVE 2: WESTERN & NORTHERN EUROPEAN SISTER HUBS
        # =========================================================================
        GeographicWaveCity(
            city_id="city_amsterdam",
            city_name="Amsterdam",
            country="Netherlands",
            wave_tier=2,
            hub_type="Dutch Electronic Capital",
            flagship_venues=[
                {"id": "ven_shelter_amsterdam", "name": "Shelter Amsterdam", "sound": "Funktion-One subterranean horn system", "desc": "Subterranean acoustic bunker underneath the A'DAM Tower in Noord."},
                {"id": "ven_garage_noord", "name": "Garage Noord", "sound": "Intimate DIY Industrial Rig", "desc": "Car repair shop transformed into avant-garde club and restaurant."},
                {"id": "ven_radion_amsterdam", "name": "RADION Amsterdam", "sound": "d&b audiotechnik Multi-Space System", "desc": "Cultural center and raw marathon techno labyrinth in Nieuw-West."},
            ],
            collectives=[
                {"id": "coll_dekmantel_ams", "name": "Dekmantel Festival Collective", "desc": "Pioneering Dutch curator shaping global selector culture and digging ethics."},
            ],
            record_stores=[
                {"id": "store_rush_hour_ams", "name": "Rush Hour Records", "desc": "Spuistraat temple of house, soul, Surinamese disco, and Detroit imports."},
            ],
            connected_corridor_cities=["city_berlin", "city_london", "city_cologne", "city_brussels"],
            acoustic_signature="High-fidelity rhythmic house, electro, and modular deep techno (125-135 BPM)",
        ),
        GeographicWaveCity(
            city_id="city_brussels",
            city_name="Brussels & Ghent",
            country="Belgium",
            wave_tier=2,
            hub_type="Belgian EBM & Rave Lineage",
            flagship_venues=[
                {"id": "ven_fuse_brussels", "name": "Fuse Brussels", "sound": "L-Acoustics K3 Club Array", "desc": "Belgium's premier techno institution since 1994, the home of Charlotte de Witte."},
                {"id": "ven_c12_brussels", "name": "C12", "sound": "Custom Audiophile Horns", "desc": "Underground railway tunnel complex by Gare Centrale for queer electronic culture."},
                {"id": "ven_kompass_ghent", "name": "Kompass Klub (Ghent)", "sound": "Funktion-One Monster Rig", "desc": "Raw industrial hangar club known for multi-day dark techno sessions."},
            ],
            collectives=[
                {"id": "coll_kntxt_belgium", "name": "KNTXT / Lenske Roster", "desc": "High-octane Belgian techno movement dominating global festival stages."},
            ],
            record_stores=[
                {"id": "store_crevette_brussels", "name": "Crevette Records", "desc": "Marolles neighborhood record store, distribution center, and selector bar."},
            ],
            connected_corridor_cities=["city_amsterdam", "city_paris", "city_london", "city_cologne"],
            acoustic_signature="Industrial EBM basslines, driving 138-144 BPM rave stabs, and dark acid",
        ),
        GeographicWaveCity(
            city_id="city_zurich",
            city_name="Zurich & Basel",
            country="Switzerland",
            wave_tier=2,
            hub_type="Alpine High-End Electronic Hub",
            flagship_venues=[
                {"id": "ven_zukunft_zurich", "name": "Zukunft", "sound": "Audiophile Wood & Rotary Console", "desc": "Intimate basement club famous for deep house, disco, and jazz-infused electronics."},
                {"id": "ven_elysia_basel", "name": "Elysia (Basel)", "sound": "Custom 4-Point Lambda Labs QX-3 Sound System", "desc": "Acclaimed worldwide as one of the most acoustically pure soundrooms ever engineered."},
            ],
            collectives=[
                {"id": "coll_nordstern_swiss", "name": "Nordstern Ship Collective", "desc": "Rhine river cruise vessel turned international high-end club."},
            ],
            record_stores=[
                {"id": "store_hum_records_zurich", "name": "Hum Records Zurich", "desc": "Specialist shop for hip-hop, rare groove, and underground house vinyl."},
            ],
            connected_corridor_cities=["city_frankfurt", "city_munich", "city_milan", "city_paris"],
            acoustic_signature="Pristine Lambda Labs acoustic dynamics, organic house, and micro-groove (120-128 BPM)",
        ),

        # =========================================================================
        # WAVE 3: MEDITERRANEAN & CAUCASUS AXIS
        # =========================================================================
        GeographicWaveCity(
            city_id="city_tbilisi",
            city_name="Tbilisi",
            country="Georgia",
            wave_tier=3,
            hub_type="Caucasus Techno Revolution",
            flagship_venues=[
                {"id": "ven_bassiani_tbilisi", "name": "Bassiani", "sound": "Funktion-One Dynamic Concrete Vault Array", "desc": "Historic Dinamo Arena swimming pool converted into the world's most intense dark techno temple."},
                {"id": "ven_khidi_tbilisi", "name": "Khidi", "sound": "Void Acoustics Industrial Bridge Rig", "desc": "Brutalist Vakhushti Bagrationi bridge vault dedicated to industrial live acts and EBM."},
                {"id": "ven_cafe_gallery_tbilisi", "name": "Cafe Gallery", "sound": "Warm Community PA", "desc": "Pioneering queer-safe space and intimate daytime dancefloor in Tbilisi."},
            ],
            collectives=[
                {"id": "coll_horoom_tbilisi", "name": "Horoom Queer Nights", "desc": "Activist queer dance collective within Bassiani advancing human rights and artistic expression."},
            ],
            record_stores=[
                {"id": "store_vodkast_tbilisi", "name": "Vodkast Records", "desc": "Independent Georgian vinyl label and electronic culture store."},
            ],
            connected_corridor_cities=["city_berlin", "city_kyiv", "city_istanbul", "city_warsaw"],
            acoustic_signature="Monolithic industrial concrete sub-bass, 142-150 BPM driving kicks, and Georgian vocal textures",
        ),
        GeographicWaveCity(
            city_id="city_barcelona",
            city_name="Barcelona",
            country="Spain",
            wave_tier=3,
            hub_type="Catalan Sound & Innovation Capital",
            flagship_venues=[
                {"id": "ven_nitsa_bcn", "name": "Nitsa Club (Sala Apolo)", "sound": "d&b audiotechnik Theater Array", "desc": "Historic 1940s dancehall housing Barcelona's longest-running underground club night."},
                {"id": "ven_moog_bcn", "name": "Moog Club", "sound": "Raw Subterranean PA", "desc": "Narrow 2-story alleyway club off Las Ramblas delivering 365 nights of techno a year."},
                {"id": "ven_input_bcn", "name": "INPUT High Fidelity Dance Club", "sound": "Funktion-One Full Surround", "desc": "Audiophile visual and sound warehouse at Poble Espanyol."},
            ],
            collectives=[
                {"id": "coll_sonar_d_bcn", "name": "Sónar+D Innovation Collective", "desc": "Global congress for creative technologies, AI music, and electronic performance."},
            ],
            record_stores=[
                {"id": "store_discos_paradiso", "name": "Discos Paradiso", "desc": "El Raval vinyl institution for electronic music, synth modulars, and dubplates."},
            ],
            connected_corridor_cities=["city_berlin", "city_amsterdam", "city_madrid", "city_lisbon", "city_rome"],
            acoustic_signature="Warm Mediterranean tech-house, modular ambient, and peak-time warehouse techno (126-136 BPM)",
        ),
        GeographicWaveCity(
            city_id="city_lisbon",
            city_name="Lisbon",
            country="Portugal",
            wave_tier=3,
            hub_type="Lusophone Bass & Atlantic Gateway",
            flagship_venues=[
                {"id": "ven_lux_lisbon", "name": "Lux Frágil", "sound": "Custom Turbosound Atlantic Array", "desc": "Riverside docklands palace founded by Manuel Reis; the jewel of Portuguese club culture."},
                {"id": "ven_ministerium_lisbon", "name": "Ministerium Club", "sound": "Funktion-One Vault", "desc": "18th-century Ministry of Finance vaulted building on Praça do Comércio."},
                {"id": "ven_nada_temple_lisbon", "name": "Nada Temple", "sound": "Industrial Techno Soundfield", "desc": "Marvila warehouse sanctuary for underground rave and hard techno."},
            ],
            collectives=[
                {"id": "coll_principe_lisbon", "name": "Príncipe Discos Collective", "desc": "Pioneering label releasing Lisbon's afro-descendant batida, tarraxinha, and kuduro."},
            ],
            record_stores=[
                {"id": "store_carpet_sniffer_lisbon", "name": "Carpet & Snares Records", "desc": "Jorge Caiado's Espaço Chiado vinyl haven dedicated to deep house and techno."},
            ],
            connected_corridor_cities=["city_madrid", "city_barcelona", "city_london", "city_sao_paulo"],
            acoustic_signature="Batida syncopations, Angolan-Portuguese kuduro polyrhythms, and Atlantic deep house (128-140 BPM)",
        ),
    ]

    def expand_concentric_wavefront(
        self, industry_graph: MusicIndustryGraph, max_wave: int = 3
    ) -> Dict[str, Any]:
        """Expand outward from Berlin to all neighboring and continental hubs up to max_wave."""
        graph = industry_graph.graph
        stats = {
            "cities_added": 0,
            "venues_added": 0,
            "collectives_added": 0,
            "record_stores_added": 0,
            "intercity_corridor_edges_added": 0,
            "max_wave_reached": max_wave,
        }

        for city_data in self.WAVE_EXPANSION_CATALOG:
            if city_data.wave_tier > max_wave:
                continue

            cid = city_data.city_id
            # 1. Ingest City Node
            if cid not in graph:
                city_ent = BaseEntity(
                    id=cid,
                    name=city_data.city_name,
                    entity_type=EntityType.TRACK,  # General entity representation
                    country=city_data.country,
                    description=f"{city_data.city_name} is an influential {city_data.hub_type} in Wave {city_data.wave_tier}. Acoustic signature: {city_data.acoustic_signature}.",
                    attributes={
                        "category": "Global Geographic Hub",
                        "wave_tier": city_data.wave_tier,
                        "hub_type": city_data.hub_type,
                        "acoustic_signature": city_data.acoustic_signature,
                    },
                )
                industry_graph.add_entity(city_ent)
                stats["cities_added"] += 1

            # 2. Ingest Flagship Venues
            for v in city_data.flagship_venues:
                vid = v["id"]
                if vid not in graph:
                    v_ent = BaseEntity(
                        id=vid,
                        name=v["name"],
                        entity_type=EntityType.VENUE if hasattr(EntityType, "VENUE") else EntityType.TRACK,
                        country=city_data.country,
                        description=v["desc"],
                        attributes={
                            "city": city_data.city_name,
                            "sound_system": v["sound"],
                            "wave_tier": city_data.wave_tier,
                        },
                    )
                    industry_graph.add_entity(v_ent)
                    stats["venues_added"] += 1

                # Link venue to city
                if not graph.has_edge(vid, cid):
                    graph.add_edge(vid, cid, rel_type="LOCATED_IN_CITY", weight=1.0)

            # 3. Ingest Collectives
            for c in city_data.collectives:
                clid = c["id"]
                if clid not in graph:
                    c_ent = BaseEntity(
                        id=clid,
                        name=c["name"],
                        entity_type=EntityType.ARTIST,
                        country=city_data.country,
                        description=c["desc"],
                        attributes={"city": city_data.city_name, "wave_tier": city_data.wave_tier},
                    )
                    industry_graph.add_entity(c_ent)
                    stats["collectives_added"] += 1

                if not graph.has_edge(clid, cid):
                    graph.add_edge(clid, cid, rel_type="BASED_IN_CITY_HUB", weight=1.0)

            # 4. Ingest Record Stores
            for r in city_data.record_stores:
                rid = r["id"]
                if rid not in graph:
                    r_ent = BaseEntity(
                        id=rid,
                        name=r["name"],
                        entity_type=EntityType.RECORD_LABEL,
                        country=city_data.country,
                        description=r["desc"],
                        attributes={"city": city_data.city_name, "wave_tier": city_data.wave_tier},
                    )
                    industry_graph.add_entity(r_ent)
                    stats["record_stores_added"] += 1

                if not graph.has_edge(rid, cid):
                    graph.add_edge(rid, cid, rel_type="LOCATED_IN_CITY", weight=1.0)

            # 5. Build Inter-City Geographic Corridor Edges
            for neighbor_id in city_data.connected_corridor_cities:
                if neighbor_id in graph and not graph.has_edge(cid, neighbor_id):
                    graph.add_edge(
                        cid,
                        neighbor_id,
                        rel_type="GEOGRAPHIC_CORRIDOR",
                        weight=0.9,
                        wave_tier=city_data.wave_tier,
                    )
                    stats["intercity_corridor_edges_added"] += 1

        logger.info(
            "Concentric Wave-Front Expansion (Up to Wave %d): Ingested %d cities, %d venues, %d collectives, %d stores, %d corridors.",
            max_wave,
            stats["cities_added"],
            stats["venues_added"],
            stats["collectives_added"],
            stats["record_stores_added"],
            stats["intercity_corridor_edges_added"],
        )

        return stats
