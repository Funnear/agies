"""Emerging Artist Pathways & Micro-Insights Engine.

Provides tactical, algorithmic career navigation for early-career musicians:
1. Optimal Distribution & Revenue Stack (Mechanical + Performance + Direct-to-Fan)
2. Curated Discovery Gateways (COLORS, Boiler Room, Tiny Desk, BBC Introducing)
3. High-Conversion A&R Showcase Festivals (Reeperbahn, The Great Escape, SXSW, ESNS)
4. Mel-Tempogram Acoustic Targets (Spectral Centroid, BPM Window, Dynamic Range)
5. 4-Phase Stepping-Stone Roadmap (DIY -> Local -> Curation -> Boutique Label)
6. Critical Traps & Warning Checklist (360 predatory deals, uncollected PRO rights, bot playlists)
"""

import logging
from typing import Any, Dict

logger = logging.getLogger("agies.analytics.emerging_pathways")


class EmergingArtistAdvisor:
    """Generates personalized micro-pathway playbooks for early-career musicians."""

    GENRE_PLAYBOOKS: Dict[str, Dict[str, Any]] = {
        "techno": {
            "recommended_bpm_range": [128.0, 138.0],
            "acoustic_profile": "Heavy low-end energy (40-90Hz), crisp hi-hat transient attack, tight dynamic control",
            "ideal_distribution_stack": [
                {
                    "platform": "Bandcamp",
                    "role": "Primary Monetization (WAV/FLAC direct sales, DJ downloads)",
                    "revenue_share": "80-85%",
                },
                {
                    "platform": "DistroKid / Proton",
                    "role": "Global DSP Streaming & Beatport delivery",
                    "revenue_share": "100% Master",
                },
                {
                    "platform": "SoundCloud Next Pro",
                    "role": "DJ promo mixes, unreleased IDs, club community seeding",
                    "revenue_share": "Monetized streams",
                },
            ],
            "top_curation_gateways": [
                {
                    "name": "Boiler Room",
                    "conversion": "Elite underground club credibility & promoter booking",
                },
                {
                    "name": "HATE (YouTube / SoundCloud)",
                    "conversion": "Direct dark/industrial techno audience reach (300k+ subscribers)",
                },
                {
                    "name": "Cercle",
                    "conversion": "Cinematic visual streaming for melodic/progressive techno",
                },
            ],
            "key_showcase_festivals": [
                "Reeperbahn Festival (Hamburg)",
                "Sónar+D (Barcelona)",
                "ADE (Amsterdam Dance Event)",
            ],
            "stepping_stone_labels": [
                "Ostgut Ton",
                "Tresor",
                "Kompakt",
                "Boysnoize Records",
                "Innervisions",
            ],
            "rights_checklist": [
                "Register works with GEMA / PRS for public performance royalties",
                "Claim neighboring rights on DJ club plays via GVL / PPL",
            ],
            "critical_traps": [
                "Signing perpetual master buyouts to small digital labels for zero advance",
                "Failing to register track metadata (ISRC codes) before DJ promo distribution",
            ],
        },
        "house": {
            "recommended_bpm_range": [120.0, 126.0],
            "acoustic_profile": "Warm low-mid bass groove (120-250Hz), swing-quantized percussion, vocal sample hooks",
            "ideal_distribution_stack": [
                {
                    "platform": "Bandcamp / Traxsource",
                    "role": "DJ community purchases & extended club mixes",
                    "revenue_share": "80-85%",
                },
                {
                    "platform": "DistroKid",
                    "role": "DSP Streaming (Spotify House Playlists, Apple Music)",
                    "revenue_share": "100% Master",
                },
            ],
            "top_curation_gateways": [
                {
                    "name": "Defected Radio / In The House",
                    "conversion": "Global house community benchmark",
                },
                {
                    "name": "Selected.",
                    "conversion": "Deep house and melodic streaming powerhouse",
                },
                {
                    "name": "Boiler Room",
                    "conversion": "Live set viral clips for club resident bookings",
                },
            ],
            "key_showcase_festivals": [
                "ADE (Amsterdam)",
                "Reeperbahn Festival",
                "c/o pop (Cologne)",
            ],
            "stepping_stone_labels": [
                "Defected",
                "Toolroom",
                "Spinnin' Deep",
                "Kitsuné Musique",
            ],
            "rights_checklist": [
                "Clear all vocal samples before commercial DSP delivery to prevent automated takedowns",
                "Register composition splits with PRO immediately upon release",
            ],
            "critical_traps": [
                "Using uncleared splice/vocal samples in streaming releases",
                "Paying third-party 'pay-for-play' Spotify promo services that trigger fraud strikes",
            ],
        },
        "indie_pop": {
            "recommended_bpm_range": [105.0, 125.0],
            "acoustic_profile": "Intimate vocal presence (1-4kHz), organic acoustic guitar/piano textures, wide stereo field",
            "ideal_distribution_stack": [
                {
                    "platform": "DistroKid / TuneCore",
                    "role": "Global DSP distribution & TikTok sound catalog",
                    "revenue_share": "100% Master",
                },
                {
                    "platform": "Bandcamp",
                    "role": "Limited cassette/vinyl runs & core fan patron membership",
                    "revenue_share": "80-85%",
                },
            ],
            "top_curation_gateways": [
                {
                    "name": "COLORSxSTUDIOS",
                    "conversion": "Global aesthetic visual breakout platform",
                },
                {
                    "name": "BBC Introducing",
                    "conversion": "Radio 1 airplay & UK festival stage slots (Glastonbury, Reading)",
                },
                {
                    "name": "NPR Tiny Desk Concert Contest",
                    "conversion": "Direct North American grassroots touring credibility",
                },
            ],
            "key_showcase_festivals": [
                "The Great Escape (Brighton)",
                "Reeperbahn Festival (Hamburg)",
                "SXSW (Austin)",
                "c/o pop (Cologne)",
            ],
            "stepping_stone_labels": [
                "Secretly Canadian",
                "Transgressive",
                "Domino",
                "Because Music",
                "Rough Trade",
            ],
            "rights_checklist": [
                "Publishing administration via Songtrust / Sentric to collect global micro-sync & lyric royalties",
                "Register with SoundExchange (US) for non-interactive radio royalties",
            ],
            "critical_traps": [
                "Signing long-term 360 merchandise/touring commission deals before establishing leverage",
                "Ignoring sync licensing opportunities in independent films, games, and streaming series",
            ],
        },
        "neo_soul": {
            "recommended_bpm_range": [75.0, 95.0],
            "acoustic_profile": "Warm analog low-end, unquantized jazzy chords, dynamic vocal nuance, dry room acoustics",
            "ideal_distribution_stack": [
                {
                    "platform": "Bandcamp",
                    "role": "Core vinyl/merch community & direct patronage",
                    "revenue_share": "85%",
                },
                {
                    "platform": "DistroKid",
                    "role": "DSP playlisting (Butter, Soul Lounge, R&B Weekly)",
                    "revenue_share": "100%",
                },
            ],
            "top_curation_gateways": [
                {
                    "name": "COLORSxSTUDIOS",
                    "conversion": "High-aesthetic global streaming breakthrough",
                },
                {
                    "name": "Soulection Radio",
                    "conversion": "The sound of tomorrow / global neo-soul tastemaker community",
                },
                {
                    "name": "NPR Tiny Desk",
                    "conversion": "Viral organic acoustic discovery",
                },
            ],
            "key_showcase_festivals": ["The Great Escape", "SXSW", "Eurosonic ESNS"],
            "stepping_stone_labels": [
                "Soulection",
                "Stones Throw",
                "Erased Tapes",
                "Brainfeeder",
            ],
            "rights_checklist": [
                "Register mechanical reproduction rights with PRO",
                "Register with BMI / PRS / GEMA",
            ],
            "critical_traps": [
                "Relinquishing publishing shares to beatmakers without split sheets signed at the studio session"
            ],
        },
    }

    def generate_pathway_playbook(
        self,
        genre: str,
        country: str = "Germany",
        career_stage: str = "bedroom_producer",  # 'bedroom_producer', 'local_gigging', 'breakthrough_ready'
    ) -> Dict[str, Any]:
        """Produce actionable tactical roadmap for an emerging musician."""
        g_key = genre.lower().replace(" ", "_")
        playbook = self.GENRE_PLAYBOOKS.get(g_key, self.GENRE_PLAYBOOKS["indie_pop"])

        # Regional collection society pairing
        rights_org = (
            "GEMA (Germany)"
            if "germany" in country.lower()
            else (
                "PRS for Music / PPL (UK)"
                if "uk" in country.lower()
                else "ASCAP / BMI / SoundExchange (USA)"
            )
        )

        # 4-Phase Roadmap
        phases = [
            {
                "phase": "Phase 1: Zero-Debt Production & Acoustic Calibration",
                "tactics": [
                    f"Calibrate track tempo within the optimal {playbook['recommended_bpm_range'][0]}-{playbook['recommended_bpm_range'][1]} BPM window for algorithmic playlist clustering.",
                    f"Acoustic Target: {playbook['acoustic_profile']}.",
                    "Sign split sheets immediately with all vocalists, co-writers, and session players prior to mastering.",
                ],
            },
            {
                "phase": "Phase 2: Direct-to-Fan Distribution & Royalties Setup",
                "tactics": [
                    f"Register composition with {rights_org} before public release.",
                    f"Deploy multi-tier distribution: Use {playbook['ideal_distribution_stack'][0]['platform']} for direct fan sales + DistroKid for DSP reach.",
                    "Embed high-resolution ISRC and ISWC metadata into WAV files.",
                ],
            },
            {
                "phase": "Phase 3: Grassroots Curation & Showcase Infiltration",
                "tactics": [
                    "Pitch unreleased track 4 weeks prior via Spotify for Artists and SubmitHub to targeted curators.",
                    f"Submit live video applications to {playbook['top_curation_gateways'][0]['name']}.",
                    f"Apply to perform at {playbook['key_showcase_festivals'][0]} during open application calls (A&R scout density: >90%).",
                ],
            },
            {
                "phase": "Phase 4: Boutique Label Leverage & Upstreaming",
                "tactics": [
                    f"Target boutique stepping-stone imprints ({', '.join(playbook['stepping_stone_labels'][:3])}) with existing track data proof.",
                    "Retain 100% of publishing ownership and negotiate a single-album or EP licensing deal with a maximum 3-year term.",
                ],
            },
        ]

        return {
            "target_genre": genre.title(),
            "target_region": country.title(),
            "career_stage": career_stage.replace("_", " ").title(),
            "recommended_bpm_range": playbook["recommended_bpm_range"],
            "acoustic_profile": playbook["acoustic_profile"],
            "distribution_stack": playbook["ideal_distribution_stack"],
            "curation_gateways": playbook["top_curation_gateways"],
            "showcase_festivals": playbook["key_showcase_festivals"],
            "stepping_stone_labels": playbook["stepping_stone_labels"],
            "rights_organization": rights_org,
            "rights_checklist": playbook["rights_checklist"],
            "critical_traps_to_avoid": playbook["critical_traps"],
            "step_by_step_roadmap": phases,
        }
