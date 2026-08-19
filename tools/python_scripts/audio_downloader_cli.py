"""CLI utility for searching and downloading audio files across registered sources.

Usage:
    python tools/python_scripts/audio_downloader_cli.py --query "ambient piano" --provider jamendo --limit 3
    python tools/python_scripts/audio_downloader_cli.py --query "birds" --provider wikimedia_commons --limit 2 --download
"""

import argparse
from pathlib import Path
import sys

# Ensure src is in pythonpath
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from agies.audio.manager import AudioSourcesManager


def main():
    parser = argparse.ArgumentParser(description="AGIES Audio Data Sources CLI")
    parser.add_argument(
        "--query", "-q", type=str, default="electronic", help="Search query or keyword"
    )
    parser.add_argument(
        "--provider",
        "-p",
        type=str,
        default=None,
        help="Target audio provider (jamendo, freesound, archive_org, musopen, wikimedia_commons, local)",
    )
    parser.add_argument(
        "--limit", "-l", type=int, default=5, help="Max results per provider"
    )
    parser.add_argument(
        "--download",
        "-d",
        action="store_true",
        help="Download matching tracks to output directory",
    )
    parser.add_argument(
        "--outdir",
        "-o",
        type=str,
        default="./downloads",
        help="Output directory for downloads",
    )
    parser.add_argument(
        "--list-sources", action="store_true", help="List all available audio sources"
    )

    args = parser.parse_args()

    if args.list_sources:
        sources = AudioSourcesManager.list_available_sources()
        print("Available Audio Data Sources:")
        for s in sources:
            print(f"  - {s}")
        return

    manager = AudioSourcesManager()
    print(
        f"Searching audio for '{args.query}' (Provider: {args.provider or 'ALL'})...\n"
    )

    tracks = manager.search(
        query=args.query, provider=args.provider, limit_per_provider=args.limit
    )

    if not tracks:
        print("No tracks found.")
        return

    print(f"Found {len(tracks)} track(s):\n")
    for i, t in enumerate(tracks, start=1):
        print(f"[{i}] [{t.provider.upper()}] {t.title} - {t.artist}")
        print(
            f"    ID: {t.id} | License: {t.license.name} (Commercial: {t.license.is_commercial_allowed})"
        )
        print(f"    Stream/Download URL: {t.stream_url or t.download_url}")
        print()

    if args.download:
        print(f"Downloading {len(tracks)} track(s) to '{args.outdir}'...")
        for t in tracks:
            try:
                dest = manager.download_track(t, output_dir=args.outdir)
                print(f"  [OK] Saved: {dest.name}")
            except Exception as e:
                print(f"  [ERR] Failed downloading {t.title}: {e}")
        print("\nDownload complete.")


if __name__ == "__main__":
    main()
