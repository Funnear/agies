# AGIES — Data Sources & Metadata Exploration

This repository evaluates electronic music (EDM) metadata, taxonomy coverage, and audio
sample sources to support downstream sub-genre classification, audio feature engineering,
and automated dataset curation.

## Data Sources — Capability & Metadata Matrix

| Data Source | Access | Auth | Data Type | Audio? | License | Verdict |
|---|---|---|---|---|---|---|
| Kaggle: Discogs Masters (2025) | Bulk CSV, 2.38M rows | Kaggle token | Genre/style metadata | No | CC0 | **Primary** — baseline genre ontology |
| Kaggle: Discogs Electronic (1990–2000) | Bulk CSV, 34.9k rows | Kaggle token | Metadata + price/popularity | No | Open | **Secondary** — pricing/popularity signals |
| Kaggle: EDM Music Genres | Bulk CSV, 40k clips | Kaggle token | Audio + labels, pre-split | Yes (3s clips) | MIT | **Primary** — only audio+label pair found |
| MusicBrainz | REST API | None (User-Agent only) | Metadata, crowd tags | No | CC0 core / CC-BY-NC-SA tags | **Cross-reference** — validate/cross-check genres |
| Freesound | REST API | API key | Metadata + samples | Yes (samples only) | Per-file CC | **Reviewed** — sample-level, not full tracks |

### Notes

- **Discogs Masters**: `genres_genre` (15 values), `styles_style` (346 values).
  `releases.csv` (7GB) exists but not recommended — duplicate labels per pressing.
- **Discogs Electronic**: adds `have`/`want`/price fields not in Masters. `styles`
  column is multi-value (comma-separated), needs parsing.
- **EDM Music Genres**: 16 balanced subgenres, pre-split train/test — strongest
  candidate for initial model training.
- **MusicBrainz**: 1 req/sec rate limit. Tags inconsistent (`edm`, `trap edm`,
  `gaming edm` all separate).
- **Freesound**: 4,037 results for "edm" query. Confirmed sample/loop-level (builds,
  kicks), not full tracks. License per-file. Fetching already implemented in
  `agies.audio` (PR #11).

## License Notes

- **CC0** (Discogs sources): fully unrestricted, including commercial use, no
  attribution required.
- **CC BY-NC-SA 3.0** (MusicBrainz genre/tag data specifically): non-commercial only —
  requires a separate commercial license from MetaBrainz before any monetized use.
- **MIT** (EDM Music Genres): permissive, commercial use allowed, requires keeping the
  original license notice.
- **Freesound**: per-file license, must be checked individually — not one blanket
  license for the whole source.

## Provider Registration & API Key Instructions

### Kaggle (all Kaggle-hosted datasets above)

1. Create a free account at kaggle.com.
2. Account Settings → generate an API token.
3. Save it so the client reads it automatically:

```bash
   mkdir -p ~/.kaggle && echo <your_token> > ~/.kaggle/access_token && chmod 600 ~/.kaggle/access_token
```

Note: Kaggle's newer accounts show the `access_token` file method above. Older docs
online may reference a different `kaggle.json` file method — if you hit auth issues,
check Kaggle's current docs at kaggle.com/docs/api#authentication. `kagglehub` is
included in `requirements.txt`.

### MusicBrainz

No account or API key required for read-only search. Only requirement: set a
descriptive `User-Agent` header identifying the app (e.g.
`"AGIes/0.1 (your-email@example.com)"`). Respect the 1 request/second rate limit.

### Freesound

1. Create a free account at freesound.org.
2. Apply for API credentials: https://freesound.org/apiv2/apply
3. Store the key as `FREESOUND_API_KEY` in your local `.env` file — never hardcode it
   in notebooks or source files.

See also `docs/20_concept/audio_file_sources.md` (PR #11) for the full production
implementation.

## Repository Exploration Notebooks

Code for downloading, loading, and running EDA on each source lives in its own
notebook — this document covers *what* each source offers and *how to get access*;
see the linked notebook for the actual loading/analysis code.

- `notebooks/data_sources/kaggle_exploration.ipynb` — Discogs Masters, Discogs
  Electronic (1990–2000), EDM Music Genres
- `notebooks/data_sources/musicbrainz_exploration.ipynb` — MusicBrainz tag/genre
  exploration
- `notebooks/data_sources/freesound_exploration.ipynb` — Freesound EDM tag/sample
  review (4,037 results for "edm" query; confirms sample-level content, not full
  tracks)