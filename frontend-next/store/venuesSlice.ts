import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface VenueItem {
  id: string;
  name: string;
  city: string;
  cap: number;
  tier: string;
  sound: string;
  email: string;
}

interface VenuesSliceState {
  venuesList: VenueItem[];
  selectedVenue: VenueItem;
  inquiryFee: string;
  inquiryDate: string;
  inquiryReceipt: string | null;
}

const defaultVenues: VenueItem[] = [
  {
    id: "ven_berghain",
    name: "Berghain / Panorama Bar",
    city: "Berlin",
    cap: 1500,
    tier: "Hall",
    sound: "Funktion-One Custom (Double 21-inch Subs)",
    email: "booking@berghain.de",
  },
  {
    id: "ven_tresor",
    name: "Tresor Berlin",
    city: "Berlin",
    cap: 800,
    tier: "Club",
    sound: "Funktion-One Vault Acoustics",
    email: "booking@tresorberlin.com",
  },
  {
    id: "ven_schokoladen",
    name: "Schokoladen (Mitte)",
    city: "Berlin",
    cap: 150,
    tier: "Intimate Debut",
    sound: "Vintage Analog PA",
    email: "booking@schokoladen-mitte.de",
  },
  {
    id: "ven_fabric",
    name: "Fabric London",
    city: "London",
    cap: 1600,
    tier: "Hall",
    sound: "Pioneer Bodysonic Bass Floor",
    email: "programming@fabriclondon.com",
  },
  {
    id: "ven_windmill_brixton",
    name: "The Windmill (Brixton)",
    city: "London",
    cap: 150,
    tier: "Intimate Debut",
    sound: "Grassroots Club PA",
    email: "windmillbrixton@gmail.com",
  },
  {
    id: "ven_bowery_ballroom",
    name: "The Bowery Ballroom",
    city: "New York City",
    cap: 575,
    tier: "Club",
    sound: "d&b Soundscape",
    email: "booking@boweryballroom.com",
  },
];

const initialState: VenuesSliceState = {
  venuesList: defaultVenues,
  selectedVenue: defaultVenues[0],
  inquiryFee: "1800",
  inquiryDate: "2026-11-14",
  inquiryReceipt: null,
};

export const venuesSlice = createSlice({
  name: "venues",
  initialState,
  reducers: {
    setSelectedVenue: (state, action: PayloadAction<VenueItem>) => {
      state.selectedVenue = action.payload;
    },
    setInquiryFee: (state, action: PayloadAction<string>) => {
      state.inquiryFee = action.payload;
    },
    setInquiryDate: (state, action: PayloadAction<string>) => {
      state.inquiryDate = action.payload;
    },
    setInquiryReceipt: (state, action: PayloadAction<string | null>) => {
      state.inquiryReceipt = action.payload;
    },
  },
});

export const {
  setSelectedVenue,
  setInquiryFee,
  setInquiryDate,
  setInquiryReceipt,
} = venuesSlice.actions;

export default venuesSlice.reducer;
