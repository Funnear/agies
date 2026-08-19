import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface DiagnosticResult {
  bpm: number;
  subgenre: string;
  confidence: number;
  matches: { name: string; genre: string; score: number }[];
  labels: { name: string; city: string; note: string }[];
  venues: { name: string; cap: number; tier: string; sound: string }[];
  pitchEmail: string;
}

interface StudioSliceState {
  artistName: string;
  trackTitle: string;
  homeCity: string;
  targetGenre: string;
  bpm: number;
  isDiagnosing: boolean;
  diagnosticResult: DiagnosticResult;
  copiedPitch: boolean;
}

export const analyzeDemoTrack = createAsyncThunk(
  "studio/analyzeDemoTrack",
  async (
    payload: {
      artistName: string;
      trackTitle: string;
      homeCity: string;
      targetGenre: string;
    },
    { rejectWithValue }
  ) => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/audio/analyze-demo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": "agies_test_key_123",
        },
        body: JSON.stringify({
          track_title: payload.trackTitle,
          artist_name: payload.artistName,
          home_city: payload.homeCity,
          home_country: "Germany",
          subgenre_hint: payload.targetGenre,
        }),
      });

      if (!res.ok) {
        throw new Error("Analysis failed");
      }
      return await res.json();
    } catch (e: any) {
      return rejectWithValue(e.message || "Failed to analyze demo");
    }
  }
);

const initialState: StudioSliceState = {
  artistName: "Subtle Flux",
  trackTitle: "Modular Resonance (Original Cut)",
  homeCity: "Berlin",
  targetGenre: "Techno",
  bpm: 132,
  isDiagnosing: false,
  copiedPitch: false,
  diagnosticResult: {
    bpm: 132,
    subgenre: "Industrial / Melodic Techno",
    confidence: 0.945,
    matches: [
      { name: "Stephan Bodzin", genre: "Melodic Techno", score: 95.8 },
      { name: "Nils Frahm", genre: "Neo-Classical Ambient", score: 92.4 },
      { name: "Boris Brejcha", genre: "High-Tech Minimal", score: 89.7 },
    ],
    labels: [
      { name: "Ostgut Ton", city: "Berlin", note: "Direct Demo Submissions" },
      { name: "Tresor Records", city: "Berlin", note: "Vinyl & Digital Imprint" },
      { name: "Innervisions", city: "Berlin", note: "Tastemaker A&R" },
    ],
    venues: [
      { name: "Berghain / Panorama Bar", cap: 1500, tier: "Hall", sound: "Funktion-One Custom" },
      { name: "Tresor Berlin", cap: 800, tier: "Club", sound: "Funktion-One Vault" },
      { name: "Schokoladen (Mitte)", cap: 150, tier: "Intimate Debut", sound: "Vintage Analog PA" },
    ],
    pitchEmail: "",
  },
};

export const studioSlice = createSlice({
  name: "studio",
  initialState,
  reducers: {
    setArtistName: (state, action: PayloadAction<string>) => {
      state.artistName = action.payload;
    },
    setTrackTitle: (state, action: PayloadAction<string>) => {
      state.trackTitle = action.payload;
    },
    setHomeCity: (state, action: PayloadAction<string>) => {
      state.homeCity = action.payload;
    },
    setTargetGenre: (state, action: PayloadAction<string>) => {
      state.targetGenre = action.payload;
      state.bpm = action.payload === "Techno" ? 132 : action.payload === "House" ? 124 : 85;
    },
    setCopiedPitch: (state, action: PayloadAction<boolean>) => {
      state.copiedPitch = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(analyzeDemoTrack.pending, (state) => {
        state.isDiagnosing = true;
      })
      .addCase(analyzeDemoTrack.fulfilled, (state, action) => {
        state.isDiagnosing = false;
        const data = action.payload;
        state.bpm = data.detected_bpm || state.bpm;
        state.diagnosticResult = {
          bpm: data.detected_bpm || state.bpm,
          subgenre: (data.classified_subgenre || "techno").replace("_", " ").toUpperCase(),
          confidence: data.subgenre_confidence || 0.94,
          matches: (data.nearest_acoustic_artist_matches || []).map((m: any) => ({
            name: m.artist_name,
            genre: m.genres ? m.genres.join(", ") : "Electronic",
            score: Number((m.acoustic_similarity_score * 100).toFixed(1)),
          })),
          labels: (data.target_record_labels || []).map((l: any) => ({
            name: l.label_name,
            city: l.country,
            note: l.a_and_r_status,
          })),
          venues: (data.recommended_debut_venues || []).map((v: any) => ({
            name: v.venue_name,
            cap: v.capacity,
            tier: v.capacity_tier,
            sound: v.sound_system,
          })),
          pitchEmail: data.generated_booking_pitch || "",
        };
      })
      .addCase(analyzeDemoTrack.rejected, (state) => {
        state.isDiagnosing = false;
      });
  },
});

export const {
  setArtistName,
  setTrackTitle,
  setHomeCity,
  setTargetGenre,
  setCopiedPitch,
} = studioSlice.actions;

export default studioSlice.reducer;
