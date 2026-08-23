# Data Sources — Exploration Summary

## Kaggle (Discogs Data Dumps)

### Setup
1. Create a free Kaggle account: kaggle.com
2. Go to Account Settings → generate an API token
3. Save it so the client reads it automatically:
```bash
   mkdir -p ~/.kaggle && echo <your_token> > ~/.kaggle/access_token && chmod 600 ~/.kaggle/access_token
```
   (Alternative: set it as an environment variable instead — `export KAGGLE_API_TOKEN=<your_token>`)
4. Install: `pip install kagglehub`
5. Test it works: `kaggle competitions list`
6. See `kaggle_exploration.ipynb` for a working example using `download_kaggle_dataset()`

Note: Kaggle now uses this `access_token` file method (as of Aug 2026). Older docs online may reference a different `kaggle.json` file — if you hit auth issues, check Kaggle's current docs at kaggle.com/docs/api#authentication.

### Dataset: ofurkancoban/discogs-datasets-january-2025
Source: https://www.kaggle.com/datasets/ofurkancoban/discogs-datasets-january-2025?select=discogs_20250101_masters.csv
| File | Size | Genre/Style Data? | Verdict |
|---|---|---|---|
| `artists.csv` | 864 MB | ❌ No | Rejected — artist metadata only |
| `masters.csv` | ~600 MB | ✅ Yes | **Recommended** — one row per musical work |
| `releases.csv` | ~7 GB | ✅ Yes | Not tested — same columns as masters, but one row per pressing/edition (duplicate labels), not recommended |
| `labels.csv` | ~200 MB | ❌ No | Not relevant — record label metadata only |

**`masters.csv` details:**
- 2,388,270 rows total, 17 columns
- Full column list: `master_main_release`, `root_master_id`, `master_year`, `artist_id`, `artist_anv`, `artist_join`, `artist_name`, `genres_genre`, `styles_style`, `master_data_quality`, `master_notes`, `master_title`, `video_description`, `video_title`, `videos_video_duration`, `videos_video_embed`, `videos_video_src`
- Relevant columns for this project: `genres_genre` (15 broad genres), `styles_style` (346 specific styles/subgenres)
- 484,647 rows tagged Genre = "Electronic"

**Top EDM styles by count (within Electronic subset):**
| Style | Count |
|---|---|
| House | 35,312 |
| Techno | 34,085 |
| Trance | 27,506 |
| Ambient | 23,232 |
| Experimental | 23,159 |

License: CC0 (Public Domain) — https://creativecommons.org/publicdomain/zero/1.0/. No restrictions on use, including commercial use. No raw audio included, metadata only.

## MusicBrainz 

Source: https://musicbrainz.org/ws/2/release-group/
Docs: https://musicbrainz.org/doc/MusicBrainz_API
Genre list: https://musicbrainz.org/genres

### Setup
- No account or API key required for read-only search
- Only requirement: set a descriptive `User-Agent` header identifying your app (e.g., `"AGIes/0.1 (your-email@example.com)"`)
- Rate limit: max 1 request/second — must be respected or your IP may be temporarily blocked
- Endpoint used: `https://musicbrainz.org/ws/2/release-group/`

### Findings
- Searched via `tag:edm` — **5,746 total release-groups** tagged "edm" in MusicBrainz's database
- Tested a sample of 400 records (7% of total) via paginated requests
- Genre/subgenre data lives in a `tags` field — crowd-sourced/user-submitted, not a fixed curated list like Discogs' `styles_style`
- Top tags found in the 400-record sample:

| Tag | Count |
|---|---|
| edm | 380 |
| electronic | 178 |
| dance | 39 |
| trap | 26 |
| trap edm | 25 |
| pop | 23 |
| house | 19 |
| dubstep | 13 |
| hardbass | 12 |
| idm | 12 |
| trance | 9 |

- Tag naming is inconsistent/messy — e.g. `edm`, `trap edm`, `dance & edm`, `gaming edm`, `lithuanian edm` all appear as separate tags, unlike Discogs' cleaner fixed genre/style taxonomy
- No audio — metadata only, same as Discogs

### License 
- Core MusicBrainz data is CC0 (Public Domain)
- **Genre/tag data specifically is CC BY-NC-SA** (non-commercial) — would require a separate commercial license from MetaBrainz if used in a monetized product later

### Verdict
Usable as a supplementary genre-label source, but noisier/less structured than Discogs. Worth considering if broader genre coverage or crowd-sourced tagging diversity is valuable, but Discogs remains the cleaner primary option for structured genre/style labels.

