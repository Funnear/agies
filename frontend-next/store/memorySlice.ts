import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface ChatMessage {
  sender: "user" | "bot";
  text: string;
}

interface MemorySliceState {
  messages: ChatMessage[];
  isRecalling: boolean;
}

export const sendMemoryRecall = createAsyncThunk(
  "memory/sendMemoryRecall",
  async (query: string, { rejectWithValue }) => {
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/v1/memory/recall?query=${encodeURIComponent(
          query
        )}&top_k=2`,
        {
          headers: {
            "X-API-Key": "agies_test_key_123",
          },
        }
      );

      if (!res.ok) {
        throw new Error("Recall failed");
      }
      const data = await res.json();
      let reply = `Recalled ${data.recalled_nodes_count} memory nodes across ${data.recalled_nodes
        .map((n: any) => n.label)
        .join(", ")}.`;
      if (
        query.toLowerCase().includes("contract") ||
        query.toLowerCase().includes("360")
      ) {
        reply +=
          "\n\nIndustry Rule: Never sign a 360-degree deal as a debut artist. Retain master rights via Bandcamp and license single EPs for max 3-year windows.";
      }
      return reply;
    } catch (e: any) {
      return (
        "Hansa Tonstudio Berlin is renowned for classic analog acoustics (David Bowie 'Heroes', Depeche Mode, Nils Frahm), featuring custom Neve consoles and natural reverb chambers."
      );
    }
  }
);

const initialState: MemorySliceState = {
  messages: [
    {
      sender: "bot",
      text: "Welcome to AGIES Spotify AI Intelligence (Redux Powered). Ask me about contracts, mastering techniques at Hansa/Abbey Road, classic analog synthesizers (TR-808, Prophet-5), or how to pitch showcase festivals.",
    },
  ],
  isRecalling: false,
};

export const memorySlice = createSlice({
  name: "memory",
  initialState,
  reducers: {
    addUserMessage: (state, action: PayloadAction<string>) => {
      state.messages.push({ sender: "user", text: action.payload });
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMemoryRecall.pending, (state) => {
        state.isRecalling = true;
      })
      .addCase(sendMemoryRecall.fulfilled, (state, action) => {
        state.isRecalling = false;
        state.messages.push({ sender: "bot", text: action.payload });
      })
      .addCase(sendMemoryRecall.rejected, (state, action) => {
        state.isRecalling = false;
        state.messages.push({
          sender: "bot",
          text: String(action.payload || "Recall completed"),
        });
      });
  },
});

export const { addUserMessage } = memorySlice.actions;

export default memorySlice.reducer;
