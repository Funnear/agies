# AGIES — Data Sources & Metadata Exploration

This repository evaluates electronic music (EDM) metadata, taxonomy coverage, and audio
sample sources to support downstream sub-genre classification, audio feature engineering,
and automated dataset curation.

## Data Sources — Capability & Metadata Matrix

| Data Source | Access | Auth | Data Type | Audio? | License | Url |
| --- | --- | --- | --- | --- | --- | --- |
| Kaggle: Discogs Masters (2025) | Bulk CSV, 2.38M rows | Kaggle token | Genre/style metadata | No | CC0 | [Kaggle](https://www.kaggle.com/datasets/ofurkancoban/discogs-datasets-january-2025) |
| Kaggle: Discogs Electronic (1990–2000) | Bulk CSV, 34.9k rows | Kaggle token | Metadata + price/popularity | No | Open | [Kaggle](https://www.kaggle.com/datasets/justinpakzad/discogs-electronic-music-dataset-1990-2000) |
| Kaggle: EDM Music Genres | Bulk CSV, 40k clips | Kaggle token | Audio + labels, pre-split | Yes (3s clips) | MIT | [Kaggle](https://www.kaggle.com/datasets/sivadithiyan/edm-music-genres) |
| MusicBrainz | REST API | None (User-Agent only) | Metadata, crowd tags | No | CC0 core / CC-BY-NC-SA tags | [API](https://musicbrainz.org/ws/2/release-group/) [Docs](https://musicbrainz.org/doc/MusicBrainz_API) |
| Freesound | REST API | API key | Metadata + samples | Yes (samples only) | Per-file CC | [API](https://freesound.org/apiv2/) [Docs](https://freesound.org/docs/api/) |
| Last.fm | REST API | API key | Metadata + crowdsourced tags | No | Non-commercial | [API](https://www.last.fm/api) [Docs](https://www.last.fm/api/show/tag.getTopTracks) |
| Wikidata | SPARQL Endpoint | None (User-Agent only) | Ontological Graph & Sub-genres | No | CC0 | [SPARQL](https://query.wikidata.org/sparql) [Docs](https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service) |

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
- **Last.fm**: High-resolution user tags (`tag.getTopTracks`, `artist.getTopTags`).
Contains nested attributes (`name`, `artist`, `mbid`, `url`, `@attr`). Useful for
multi-label genre classification and artist similarity graphs.
- **Wikidata**: Graph-based ontological query service (`wd:Q212805` for EDM).
 Uses SPARQL property paths (`wdt:P279*` for subclass hierarchy, 
 `wdt:P136` for artist genre tags) to fetch structured parent-child 
 sub-genre relationships. Requires custom `User-Agent` identification header.

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
2. Apply for API credentials: <https://freesound.org/apiv2/apply>
3. Store the key as `FREESOUND_API_KEY` in your local `.env` file — never hardcode it
   in notebooks or source files.

See also `docs/20_concept/audio_file_sources.md` (PR #11) for the full production
implementation.

### Last.fm API Key

1. Register a free account at `last.fm`.
2. Apply for credentials at `last.fm/api/account/create`
(Application Name: `AGIES Data Exploration`).
3. Copy the generated API Key.
4. Store the key as `LASTFM_API_KEY` in your local `.env` file — never hardcode it
in notebooks or source files.

### Wikidata SPARQL Endpoint

No account or API key required. Requests require a custom `User-Agent` header 
(e.g. `"AGIES/0.1 (info@dataravers.space)"`) and 
`Accept: application/sparql-results+json`.

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
- `notebooks/data_sources/lastfm_exploration.ipynb` — Last.fm EDM tag/track metadata
exploration (queries `tag.getTopTracks`, evaluates MBID link coverage,
and checks raw nested payload structure).
- `notebooks/data_sources/wikidata_exploration.ipynb` — Wikidata SPARQL EDM sub-genre taxonomy,
 graph hierarchy, and artist attribute mapping.
