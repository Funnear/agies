import { configureStore } from "@reduxjs/toolkit";
import { TypedUseSelectorHook, useDispatch, useSelector } from "react-redux";
import playerReducer from "./playerSlice";
import studioReducer from "./studioSlice";
import venuesReducer from "./venuesSlice";
import memoryReducer from "./memorySlice";

export const store = configureStore({
  reducer: {
    player: playerReducer,
    studio: studioReducer,
    venues: venuesReducer,
    memory: memoryReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
