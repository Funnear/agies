import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface AudioSnippetData {
  title: string;
  snippet_url: string;
  duration_sec: number;
  file_format: string;
  is_downloaded: boolean;
  local_path?: string;
  detected_bpm: number;
  subgenre: string;
  acoustic_energy: number;
}

export interface DiscoveredArtistProfile {
  artist_slug: string;
  artist_name: string;
  website_url: string;
  home_city: string;
  home_country: string;
  genres: string[];
  bio_snippet: string;
  audio_snippets: AudioSnippetData[];
  acoustic_signature: {
    detected_bpm: number;
    classified_subgenre: string;
    mel_spectral_energy?: number;
    tempogram_harmonic_strength?: number;
  };
  matched_venues: {
    venue_id: string;
    venue_name: string;
    city: string;
    country: string;
    capacity: number;
    capacity_tier: string;
    sound_system: string;
    booking_email: string;
    acoustic_fit_score: number;
    recommended_slot: string;
  }[];
}

interface DiscoveryState {
  crawledUrl: string;
  isCrawling: boolean;
  discoveredArtists: DiscoveredArtistProfile[];
  selectedDiscoveredArtist: DiscoveredArtistProfile | null;
}

export const fetchDiscoveryFeed = createAsyncThunk(
  "discovery/fetchDiscoveryFeed",
  async (_, { rejectWithValue }) => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/discovery/artist-feed", {
        headers: { "X-API-Key": "agies_test_key_123" },
      });
      if (!res.ok) throw new Error("Failed to fetch discovery feed");
      return await res.json();
    } catch (e: any) {
      return rejectWithValue(e.message);
    }
  }
);

export const crawlArtistWebsite = createAsyncThunk(
  "discovery/crawlArtistWebsite",
  async (
    payload: {
      website_url: string;
      artist_name?: string;
      home_city?: string;
      genre_hint?: string;
    },
    { rejectWithValue }
  ) => {
    try {
      const res = await fetch(
        "http://127.0.0.1:8000/api/v1/discovery/crawl-artist-website",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-API-Key": "agies_test_key_123",
          },
          body: JSON.stringify(payload),
        }
      );
      if (!res.ok) throw new Error("Failed to crawl website");
      return await res.json();
    } catch (e: any) {
      return rejectWithValue(e.message);
    }
  }
);

const defaultSeeds: DiscoveredArtistProfile[] = [
  {
    artist_slug: "nils-frahm",
    artist_name: "Nils Frahm",
    website_url: "https://www.nilsfrahm.com",
    home_city: "Berlin",
    home_country: "Germany",
    genres: ["Neo-Classical", "Ambient", "Modular Synth"],
    bio_snippet:
      "Berlin-based composer recording at Funkhaus Berlin Saal 3 with custom pianos and Roland Space Echoes.",
    audio_snippets: [
      {
        title: "Says (Modular Extract)",
        snippet_url: "https://stream.agies.network/snippets/nils-frahm/says.mp3",
        duration_sec: 30,
        file_format: "wav",
        is_downloaded: true,
        detected_bpm: 110,
        subgenre: "ambient",
        acoustic_energy: 0.82,
      },
    ],
    acoustic_signature: {
      detected_bpm: 110,
      classified_subgenre: "ambient",
      mel_spectral_energy: 0.82,
    },
    matched_venues: [
      {
        venue_id: "ven_funkhaus",
        venue_name: "Funkhaus Berlin (Saal 1)",
        city: "Berlin",
        country: "Germany",
        capacity: 1500,
        capacity_tier: "hall",
        sound_system: "Vintage Studio Acoustics & d&b audiotechnik",
        booking_email: "events@funkhaus-berlin.net",
        acoustic_fit_score: 99.4,
        recommended_slot: "Headliner",
      },
    ],
  },
  {
    artist_slug: "tycho",
    artist_name: "Tycho (Scott Hansen)",
    website_url: "https://tychomusic.com",
    home_city: "San Francisco",
    home_country: "United States",
    genres: ["Chillwave", "Downtempo", "Ambient Electronic"],
    bio_snippet:
      "Grammy-nominated audio-visual producer merging warm vintage analog synthesizers with atmospheric guitar textures.",
    audio_snippets: [
      {
        title: "Epoch (Live Preview)",
        snippet_url: "https://stream.agies.network/snippets/tycho/epoch.mp3",
        duration_sec: 30,
        file_format: "wav",
        is_downloaded: true,
        detected_bpm: 118,
        subgenre: "house",
        acoustic_energy: 0.88,
      },
    ],
    acoustic_signature: {
      detected_bpm: 118,
      classified_subgenre: "house",
      mel_spectral_energy: 0.88,
    },
    matched_venues: [
      {
        venue_id: "ven_bowery_ballroom",
        venue_name: "The Bowery Ballroom",
        city: "New York City",
        country: "United States",
        capacity: 575,
        capacity_tier: "club",
        sound_system: "d&b Soundscape Immersive System",
        booking_email: "booking@boweryballroom.com",
        acoustic_fit_score: 96.2,
        recommended_slot: "Headliner",
      },
    ],
  },
  {
    artist_slug: "bicep",
    artist_name: "BICEP",
    website_url: "https://bicepmusic.com",
    home_city: "London",
    home_country: "United Kingdom",
    genres: ["Electronic", "Breakbeat", "Deep House"],
    bio_snippet:
      "Ninja Tune electronic duo blending 90s breakbeats, TB-303 analog acid lines, and massive festival euphoria.",
    audio_snippets: [
      {
        title: "Glue (Snippet)",
        snippet_url: "https://stream.agies.network/snippets/bicep/glue.mp3",
        duration_sec: 30,
        file_format: "wav",
        is_downloaded: true,
        detected_bpm: 128,
        subgenre: "techno",
        acoustic_energy: 0.94,
      },
    ],
    acoustic_signature: {
      detected_bpm: 128,
      classified_subgenre: "techno",
      mel_spectral_energy: 0.94,
    },
    matched_venues: [
      {
        venue_id: "ven_fabric",
        venue_name: "Fabric London",
        city: "London",
        country: "United Kingdom",
        capacity: 1600,
        capacity_tier: "hall",
        sound_system: "Pioneer Bodysonic Bass Floor",
        booking_email: "programming@fabriclondon.com",
        acoustic_fit_score: 98.6,
        recommended_slot: "Headliner",
      },
    ],
  },
];

const initialState: DiscoveryState = {
  crawledUrl: "https://tychomusic.com",
  isCrawling: false,
  discoveredArtists: defaultSeeds,
  selectedDiscoveredArtist: defaultSeeds[0],
};

export const discoverySlice = createSlice({
  name: "discovery",
  initialState,
  reducers: {
    setCrawledUrl: (state, action: PayloadAction<string>) => {
      state.crawledUrl = action.payload;
    },
    setSelectedDiscoveredArtist: (
      state,
      action: PayloadAction<DiscoveredArtistProfile>
    ) => {
      state.selectedDiscoveredArtist = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDiscoveryFeed.fulfilled, (state, action) => {
        if (action.payload && action.payload.length > 0) {
          state.discoveredArtists = action.payload;
          state.selectedDiscoveredArtist = action.payload[0];
        }
      })
      .addCase(crawlArtistWebsite.pending, (state) => {
        state.isCrawling = true;
      })
      .addCase(crawlArtistWebsite.fulfilled, (state, action) => {
        state.isCrawling = false;
        const newArtist = action.payload;
        state.discoveredArtists.unshift(newArtist);
        state.selectedDiscoveredArtist = newArtist;
      })
      .addCase(crawlArtistWebsite.rejected, (state) => {
        state.isCrawling = false;
      });
  },
});

export const { setCrawledUrl, setSelectedDiscoveredArtist } =
  discoverySlice.actions;

export default discoverySlice.reducer;
