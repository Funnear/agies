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

