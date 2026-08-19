"""CLI Assistant for Bedroom Music Producers & Early-Career Artists."""

import argparse
import logging
from pathlib import Path
import sys

# Ensure src is in pythonpath
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from agies.audio.bedroom_producer import BedroomProducerAssistant

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("agies.bedroom_cli")


def main():
    parser = argparse.ArgumentParser(
        description="AGIES AI Assistant for Bedroom Music Producers"
    )
    parser.add_argument(
        "--track",
        type=str,
        default="Subterranean Pulse",
        help="Your track or demo title",
    )
    parser.add_argument(
        "--artist", type=str, default="Resonance Alpha", help="Your artist alias"
    )
    parser.add_argument(
        "--city",
        type=str,
        default="Berlin",
        help="Your base city (e.g. Berlin, London, New York City, Paris)",
    )
    parser.add_argument(
        "--country", type=str, default="Germany", help="Your home country"
    )
    parser.add_argument(
        "--genre", type=str, default="Techno", help="Target subgenre / sound"
    )
    parser.add_argument(
        "--audio-file",
        type=str,
        default=None,
        help="Path to WAV or MP3 file for acoustic feature extraction",
    )
    args = parser.parse_args()

    assistant = BedroomProducerAssistant()
    report = assistant.analyze_demo_and_generate_dossier(
        track_title=args.track,
        artist_name=args.artist,
        home_city=args.city,
        home_country=args.country,
        subgenre_hint=args.genre,
        raw_audio_path=args.audio_file,
    )

    print("\n" + "=" * 70)
    print("      🎛️  AGIES BEDROOM PRODUCER AI A&R & CAREER DOSSIER")
    print("=" * 70)
    print(f"Artist Alias:        {report.artist_name}")
    print(f"Track Title:         '{report.track_title}'")
    print(f"Location:            {report.home_city}, {report.home_country}")
    print(
        f"Classified Subgenre: {report.classified_subgenre.replace('_', ' ').title()} ({report.subgenre_confidence * 100:.1f}% confidence)"
    )
    print(
        f"Detected BPM:        {report.detected_bpm} BPM (32 Mel bands + 48 Tempogram bins)"
    )
    print("-" * 70)

    print("🎧 TOP ACOUSTICALLY MATCHING ARTISTS IN THE KNOWLEDGE GRAPH:")
    for a in report.nearest_acoustic_artist_matches:
        print(
            f"  * {a['artist_name']} ({', '.join(a.get('genres', []))}) -> Sonic Match: {a['acoustic_similarity_score'] * 100:.1f}%"
        )

    print("\n🏢 TARGET INDIE RECORD LABELS (OPEN TO DEMOS):")
    for lbl in report.target_record_labels:
        print(f"  * {lbl['label_name']} [{lbl['country']}] -> {lbl['a_and_r_status']}")

    print("\n🏟️ RECOMMENDED DEBUT & STEPPING-STONE VENUES:")
    for v in report.recommended_debut_venues:
        print(f"  * {v['venue_name']} ({v['city']} | Cap: {v['capacity']})")
        print(f"    Booking Email: {v['booking_email']} | Sound: {v['sound_system']}")

    print("\n🗺️ YOUR 4-PHASE STEPPING-STONE ROADMAP:")
    for phase, desc in report.four_phase_roadmap.items():
        print(f"  [{phase}]")
        print(f"    -> {desc}")

    print("\n⚠️ CRITICAL TRAPS TO AVOID:")
    for trap in report.critical_traps_to_avoid:
        print(f"  * {trap}")

    print("\n📨 READY-TO-SEND BOOKING PITCH EMAIL DRAFT:")
    print("-" * 70)
    print(report.generated_booking_pitch)
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
