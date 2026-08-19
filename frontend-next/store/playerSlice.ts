import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface TrackState {
  title: string;
  artist: string;
  cover: string;
  genre: string;
  bpm: number;
  duration: string;
  progress: number;
}

interface PlayerSliceState {
  currentTrack: TrackState;
  isPlaying: boolean;
  volume: number;
  isLiked: boolean;
  showRightDrawer: boolean;
}

const initialState: PlayerSliceState = {
  currentTrack: {
    title: "Modular Resonance (Original Cut)",
    artist: "Subtle Flux",
    cover: "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=300&q=80",
    genre: "Industrial Techno",
    bpm: 132,
    duration: "4:32",
    progress: 35,
  },
  isPlaying: false,
  volume: 80,
  isLiked: true,
  showRightDrawer: true,
};

export const playerSlice = createSlice({
  name: "player",
  initialState,
  reducers: {
    setTrack: (state, action: PayloadAction<Partial<TrackState>>) => {
      state.currentTrack = { ...state.currentTrack, ...action.payload };
    },
    togglePlay: (state) => {
      state.isPlaying = !state.isPlaying;
    },
    setIsPlaying: (state, action: PayloadAction<boolean>) => {
      state.isPlaying = action.payload;
    },
    setVolume: (state, action: PayloadAction<number>) => {
      state.volume = action.payload;
    },
    toggleLike: (state) => {
      state.isLiked = !state.isLiked;
    },
    toggleRightDrawer: (state) => {
      state.showRightDrawer = !state.showRightDrawer;
    },
    setProgress: (state, action: PayloadAction<number>) => {
      state.currentTrack.progress = action.payload;
    },
  },
});

export const {
  setTrack,
  togglePlay,
  setIsPlaying,
  setVolume,
  toggleLike,
  toggleRightDrawer,
  setProgress,
} = playerSlice.actions;

export default playerSlice.reducer;
