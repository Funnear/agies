"use client";

import React, { useState, useEffect, useRef } from "react";
import { AudioVisualizer3D } from "@/components/AudioVisualizer3D";
import { NetworkGraph3D } from "@/components/NetworkGraph3D";
import { useAppDispatch, useAppSelector } from "@/store";
import {
  togglePlay,
  setIsPlaying,
  setVolume,
  toggleLike,
  toggleRightDrawer,
  setTrack,
  setProgress,
} from "@/store/playerSlice";
import {
  setArtistName,
  setTrackTitle,
  setHomeCity,
  setTargetGenre,
  analyzeDemoTrack,
} from "@/store/studioSlice";
import {
  setSelectedVenue,
  setInquiryFee,
  setInquiryDate,
  setInquiryReceipt,
  VenueItem,
} from "@/store/venuesSlice";
import { addUserMessage, sendMemoryRecall } from "@/store/memorySlice";
import {
  Home as HomeIcon,
  Radio,
  Building2,
  Share2,
  Brain,
  BarChart3,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Shuffle,
  Repeat,
  Volume2,
  VolumeX,
  Heart,
  Sparkles,
  Send,
  Copy,
  CheckCircle2,
  Globe2,
  Sliders,
  Disc3,
  Compass,
  Flame,
  Library,
  UploadCloud,
  FileAudio,
  CheckSquare,
  Square,
  FileText,
  X,
  ExternalLink,
  Music,
  Download,
} from "lucide-react";

export default function SpotifyPolishedApp() {
  const dispatch = useAppDispatch();
  const [activeNav, setActiveNav] = useState<
    "home" | "studio" | "venues" | "galaxy" | "memory" | "analytics"
  >("home");

  // Redux Global State
  const { currentTrack, isPlaying, volume, isLiked, showRightDrawer } =
    useAppSelector((state) => state.player);

  const {
    artistName,
    trackTitle,
    homeCity,
    targetGenre,
    bpm,
    isDiagnosing,
    diagnosticResult,
  } = useAppSelector((state) => state.studio);

  const { venuesList, selectedVenue, inquiryFee, inquiryDate, inquiryReceipt } =
    useAppSelector((state) => state.venues);

  const { messages: chatMessages, isRecalling } = useAppSelector(
    (state) => state.memory
  );

  // Local UI State
  const [chatInput, setChatInput] = useState("");
  const [copiedPitch, setCopiedPitch] = useState(false);
  const [showContractModal, setShowContractModal] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // DAW Stem Mixer Levels
  const [stems, setStems] = useState({
    drums: 85,
    bass: 90,
    synths: 75,
    vocals: 60,
  });

  // Roadmap Checklists
  const [completedRoadmapSteps, setCompletedRoadmapSteps] = useState<{
    [key: string]: boolean;
  }>({
    step_0: true,
    step_1: false,
    step_2: false,
    step_3: false,
  });

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  // Live Playback Simulation
  useEffect(() => {
    let interval: any = null;
    if (isPlaying) {
      interval = setInterval(() => {
        dispatch(
          setProgress((currentTrack.progress >= 100 ? 0 : currentTrack.progress + 0.5))
        );
      }, 500);
    }
    return () => clearInterval(interval);
  }, [isPlaying, currentTrack.progress, dispatch]);

  const toggleRoadmapStep = (stepKey: string) => {
    setCompletedRoadmapSteps((prev) => ({
      ...prev,
      [stepKey]: !prev[stepKey],
    }));
  };

  const playTitanTrack = (trackData: {
    title: string;
    artist: string;
    cover: string;
    genre: string;
    bpm: number;
    duration: string;
  }) => {
    dispatch(setTrack({ ...trackData, progress: 0 }));
    dispatch(setIsPlaying(true));
    showToast(`Now Playing: ${trackData.artist} — ${trackData.title}`);
  };

  const runStudioDiagnostic = () => {
    dispatch(
      analyzeDemoTrack({
        artistName,
        trackTitle,
        homeCity,
        targetGenre,
      })
    );
    dispatch(
      setTrack({
        title: trackTitle,
        artist: artistName,
        genre: targetGenre,
        bpm: bpm,
      })
    );
    showToast("Acoustic Mel-Tempogram Diagnostic Started!");
  };

  const handleSendChat = () => {
    if (!chatInput.trim()) return;
    const q = chatInput;
    dispatch(addUserMessage(q));
    setChatInput("");
    dispatch(sendMemoryRecall(q));
  };

  const pitchText = `Subject: Live Debut Pitch / Support Slot Inquiry: ${artistName} @ ${selectedVenue.name}

Hi ${selectedVenue.name} Bookings Team,

I hope you're having a great week. I'm ${artistName}, a ${homeCity}-based producer producing ${targetGenre} (sound profile: ${currentTrack.bpm} BPM, Mel-Tempogram acoustic energy aligned with Stephan Bodzin).

I've just finalized my new 3-track EP '${trackTitle}', and I'm looking to play opening support slots for your upcoming club nights.
You can listen to the private demo stream here: [Private Demo Stream Link]

I would love to be considered for an opening support slot on your lineup. Thank you for your time and for supporting grassroots music!

Best regards,
${artistName}
Contact: booking@${artistName.toLowerCase().replace(/\s+/g, "")}-official.com`;

  const copyPitch = () => {
    navigator.clipboard.writeText(pitchText);
    setCopiedPitch(true);
    showToast("Promoter Pitch copied to clipboard!");
    setTimeout(() => setCopiedPitch(false), 2000);
  };

  const dispatchBooking = () => {
    dispatch(
      setInquiryReceipt(
        `✓ Formal Booking Offer of ${inquiryFee} EUR for ${inquiryDate} transmitted to ${selectedVenue.name} Booking Dept (Logged to disk). Status: DISPATCHED_TO_AGENT.`
      )
    );
    showToast(`Booking inquiry dispatched to ${selectedVenue.name}!`);
  };

  return (
    <div className="h-screen w-screen bg-black text-[#b3b3b3] flex flex-col select-none overflow-hidden font-sans relative">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-50 px-4 py-2 rounded-full bg-[#181818] border border-[#1DB954]/40 text-white font-medium text-xs shadow-2xl flex items-center gap-2 animate-in fade-in slide-in-from-top-4 duration-200">
          <CheckCircle2 className="w-4 h-4 text-[#1DB954]" />
          {toastMessage}
        </div>
      )}

      {/* Upper Container (Sidebar + Main + Right Drawer) */}
      <div className="flex-1 flex overflow-hidden p-2 gap-2">
        {/* ========================================================= */}
        {/* 1. SPOTIFY LEFT SIDEBAR                                    */}
        {/* ========================================================= */}
        <aside className="w-64 bg-[#121212] rounded-xl flex flex-col gap-2 p-4 shrink-0 border border-white/[0.06] shadow-2xl">
          {/* Brand Header */}
          <div className="flex items-center gap-2.5 px-2 py-1.5 text-white">
            <div className="w-8 h-8 rounded-full bg-[#1DB954] flex items-center justify-center text-black font-black shadow-lg shadow-[#1DB954]/20">
              <Disc3
                className={`w-5 h-5 ${isPlaying ? "animate-spin" : ""}`}
                style={{ animationDuration: "6s" }}
              />
            </div>
            <div className="font-extrabold text-lg tracking-tight text-white flex items-center gap-1.5">
              AGIES{" "}
              <span className="text-[10px] text-[#1DB954] font-mono px-1.5 py-0.5 rounded bg-[#1DB954]/10 border border-[#1DB954]/30 font-bold">
                STUDIO PRO
              </span>
            </div>
          </div>

          {/* Primary Nav */}
          <div className="space-y-1 mt-3">
            {[
              { id: "home", label: "Home Feed", icon: HomeIcon },
              { id: "studio", label: "Bedroom Studio", icon: Radio },
              { id: "venues", label: "Venue Matchmaker", icon: Building2 },
              { id: "galaxy", label: "3D Universe", icon: Share2 },
              { id: "memory", label: "Graphify AI Chat", icon: Brain },
              { id: "analytics", label: "Industry Radar", icon: BarChart3 },
            ].map((nav) => {
              const Icon = nav.icon;
              const isActive = activeNav === nav.id;
              return (
                <button
                  key={nav.id}
                  onClick={() => setActiveNav(nav.id as any)}
                  className={`w-full flex items-center gap-4 px-3.5 py-2.5 rounded-lg font-semibold text-sm transition-all ${
                    isActive
                      ? "text-white bg-white/10 font-bold text-[#1DB954]"
                      : "hover:text-white hover:bg-white/[0.04]"
                  }`}
                >
                  <Icon
                    className={`w-4 h-4 ${
                      isActive ? "text-[#1DB954]" : "text-white/60"
                    }`}
                  />
                  {nav.label}
                </button>
              );
            })}
          </div>

          {/* Library & Corridors List */}
          <div className="flex-1 mt-4 pt-4 border-t border-white/[0.06] flex flex-col min-h-0">
            <div className="flex items-center justify-between text-[11px] font-bold uppercase tracking-wider text-white/40 px-2 mb-2">
              <span>Ecosystem Corridors</span>
              <Library className="w-3.5 h-3.5" />
            </div>
            <div className="overflow-y-auto space-y-1 pr-1 flex-1 text-xs">
              {[
                {
                  title: "Berlin ↔ London Electronic Highway",
                  sub: "Corridor • 0.98 Strength",
                },
                {
                  title: "Stockholm ↔ LA Pop Axis",
                  sub: "Corridor • 0.99 Strength",
                },
                {
                  title: "Berghain / Panorama Bar",
                  sub: "Venue • 1,500 Cap",
                },
                {
                  title: "Hansa Tonstudio",
                  sub: "Studio • Berlin Sound",
                },
                { title: "Ostgut Ton", sub: "Label • Techno Landmark" },
                {
                  title: "Reeperbahn Festival 2026",
                  sub: "A&R Showcase • 90%+ Density",
                },
              ].map((item, idx) => (
                <div
                  key={idx}
                  className="px-2.5 py-2 rounded-lg hover:bg-white/[0.06] cursor-pointer text-white/80 hover:text-white transition-all group"
                >
                  <div className="font-semibold truncate group-hover:text-[#1DB954] transition-colors">
                    {item.title}
                  </div>
                  <div className="text-[11px] text-[#b3b3b3] truncate">
                    {item.sub}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </aside>

        {/* ========================================================= */}
        {/* 2. MAIN SCROLLABLE CONTAINER                               */}
        {/* ========================================================= */}
        <main className="flex-1 bg-[#121212] rounded-xl overflow-y-auto relative border border-white/[0.06] shadow-2xl flex flex-col">
          {/* Top Sticky Bar */}
          <div className="sticky top-0 bg-[#121212]/80 backdrop-blur-xl z-30 px-6 py-3 flex items-center justify-between border-b border-white/[0.06]">
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono text-white/60 bg-black/40 px-3 py-1 rounded-full border border-white/10 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-[#1DB954] animate-pulse"></span>
                API ONLINE :8000 • REDUX TOOLKIT • 507 NODES
              </span>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => dispatch(toggleRightDrawer())}
                className="text-xs bg-white/10 hover:bg-white/20 text-white px-3.5 py-1.5 rounded-full font-semibold transition-all flex items-center gap-1.5"
              >
                <Sliders className="w-3.5 h-3.5" />{" "}
                {showRightDrawer ? "Hide Drawer" : "Show Drawer"}
              </button>
            </div>
          </div>

          <div className="p-6 flex-1 space-y-8">
            {/* ---------------------------------------------------- */}
            {/* VIEW 1: HOME FEED                                    */}
            {/* ---------------------------------------------------- */}
            {activeNav === "home" && (
              <div className="space-y-8">
                {/* Hero Banner */}
                <div className="rounded-2xl p-8 bg-gradient-to-br from-[#1e3a8a]/70 via-[#0f172a] to-[#121212] border border-blue-500/20 relative overflow-hidden shadow-2xl">
                  <div className="max-w-2xl relative z-10 space-y-4">
                    <span className="px-3 py-1 bg-[#1DB954]/20 border border-[#1DB954]/40 text-[#1DB954] rounded-full text-xs font-mono font-bold">
                      ACOUSTIC A&R INTELLIGENCE PLATFORM
                    </span>
                    <h1 className="text-4xl font-extrabold text-white tracking-tight leading-tight">
                      Take Your Bedroom Demos to Global Stages
                    </h1>
                    <p className="text-sm text-[#b3b3b3] leading-relaxed">
                      Powered by the <b>arXiv:2110.08862 Mel-Spectrogram & Tempogram Neural Classifier</b> and a 507-node Global Music Industry Graph.
                    </p>
                    <div className="flex gap-3 pt-2">
                      <button
                        onClick={() => setActiveNav("studio")}
                        className="px-6 py-3 bg-[#1DB954] hover:bg-[#1ed760] text-black font-extrabold rounded-full text-sm transition-transform active:scale-95 shadow-lg shadow-[#1DB954]/20 flex items-center gap-2"
                      >
                        <Play className="w-4 h-4 fill-black" /> Open Bedroom Studio
                      </button>
                      <button
                        onClick={() => setActiveNav("galaxy")}
                        className="px-6 py-3 bg-white/10 hover:bg-white/20 text-white font-bold rounded-full text-sm transition-all"
                      >
                        Explore 3D Galaxy
                      </button>
                    </div>
                  </div>
                </div>

                {/* Nearest Acoustic Titans */}
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-bold text-white tracking-tight">
                      Nearest Acoustic Titans (Click to Listen & Benchmark)
                    </h2>
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                    {[
                      {
                        title: "Singularity (Original Mix)",
                        artist: "Stephan Bodzin",
                        genre: "Melodic Techno",
                        score: "95.8%",
                        bpm: 126,
                        duration: "7:01",
                        cover:
                          "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&q=80",
                      },
                      {
                        title: "Says (Funkhaus Session)",
                        artist: "Nils Frahm",
                        genre: "Neo-Classical Ambient",
                        score: "92.4%",
                        bpm: 110,
                        duration: "8:18",
                        cover:
                          "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400&q=80",
                      },
                      {
                        title: "Selected Ambient Works 85-92",
                        artist: "Aphex Twin",
                        genre: "Ambient / IDM",
                        score: "91.2%",
                        bpm: 122,
                        duration: "5:44",
                        cover:
                          "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400&q=80",
                      },
                      {
                        title: "Gravity (High-Tech Minimal)",
                        artist: "Boris Brejcha",
                        genre: "High-Tech Minimal",
                        score: "89.7%",
                        bpm: 125,
                        duration: "9:24",
                        cover:
                          "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=400&q=80",
                      },
                    ].map((item, idx) => (
                      <div
                        key={idx}
                        onClick={() => playTitanTrack(item)}
                        className="bg-[#181818] hover:bg-[#242424] p-4 rounded-xl transition-all group cursor-pointer border border-white/[0.04] relative hover:-translate-y-1 hover:shadow-2xl"
                      >
                        <div className="relative mb-3 aspect-square rounded-lg overflow-hidden bg-black/40">
                          <img
                            src={item.cover}
                            alt={item.artist}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                          />
                          <button className="absolute bottom-2.5 right-2.5 w-11 h-11 rounded-full bg-[#1DB954] shadow-xl flex items-center justify-center opacity-0 group-hover:opacity-100 group-hover:translate-y-0 translate-y-2 transition-all duration-200 hover:scale-105">
                            <Play className="w-5 h-5 fill-black ml-0.5" />
                          </button>
                        </div>
                        <div className="font-bold text-white text-sm truncate">
                          {item.artist}
                        </div>
                        <div className="text-xs text-[#b3b3b3] truncate mt-0.5">
                          {item.title}
                        </div>
                        <div className="text-[11px] font-mono text-[#1DB954] font-bold mt-2 flex items-center justify-between">
                          <span>{item.score} MATCH</span>
                          <span className="text-white/40">{item.bpm} BPM</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Debut Venues */}
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-bold text-white tracking-tight">
                      Stepping-Stone Debut Venues
                    </h2>
                    <span
                      className="text-xs text-[#1DB954] font-semibold hover:underline cursor-pointer"
                      onClick={() => setActiveNav("venues")}
                    >
                      Browse Venues
                    </span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {venuesList.slice(0, 3).map((v: VenueItem, idx: number) => (
                      <div
                        key={idx}
                        onClick={() => {
                          dispatch(setSelectedVenue(v));
                          setActiveNav("venues");
                        }}
                        className="bg-[#181818] hover:bg-[#242424] p-4 rounded-xl border border-white/[0.04] transition-all cursor-pointer group hover:-translate-y-1 hover:shadow-xl"
                      >
                        <div className="flex justify-between items-start mb-2">
                          <div className="font-bold text-white text-sm group-hover:text-[#1DB954] transition-colors">
                            {v.name}
                          </div>
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-white font-bold">
                            {v.tier}
                          </span>
                        </div>
                        <div className="text-xs text-[#b3b3b3]">
                          {v.city} • Capacity: {v.cap}
                        </div>
                        <div className="text-[11px] text-white/50 mt-1 font-mono">
                          {v.sound}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* ---------------------------------------------------- */}
            {/* VIEW 2: BEDROOM STUDIO & DAW STEM MIXER              */}
            {/* ---------------------------------------------------- */}
            {activeNav === "studio" && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Left: Input Parameters & Audio Dropzone */}
                  <div className="bg-[#181818] rounded-2xl p-6 border border-white/[0.06] space-y-4 shadow-xl">
                    <div className="flex justify-between items-center pb-3 border-b border-white/10">
                      <div className="font-bold text-white flex items-center gap-2">
                        <Radio className="w-5 h-5 text-[#1DB954]" /> Demo Track Analyzer (Redux Store)
                      </div>
                      <span className="text-[10px] font-mono px-2.5 py-1 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/30 font-bold">
                        arXiv:2110.08862
                      </span>
                    </div>

                    <div className="space-y-3 text-xs">
                      <div>
                        <label className="font-bold text-white/50 uppercase tracking-wider block mb-1">
                          Artist / Project Alias
                        </label>
                        <input
                          type="text"
                          value={artistName}
                          onChange={(e) => dispatch(setArtistName(e.target.value))}
                          className="w-full bg-black/60 border border-white/10 rounded-lg p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="font-bold text-white/50 uppercase tracking-wider block mb-1">
                          Track Title
                        </label>
                        <input
                          type="text"
                          value={trackTitle}
                          onChange={(e) => dispatch(setTrackTitle(e.target.value))}
                          className="w-full bg-black/60 border border-white/10 rounded-lg p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
                        />
                      </div>
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="font-bold text-white/50 uppercase tracking-wider block mb-1">
                            City Hub
                          </label>
                          <select
                            value={homeCity}
                            onChange={(e) => dispatch(setHomeCity(e.target.value))}
                            className="w-full bg-black/60 border border-white/10 rounded-lg p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
                          >
                            <option value="Berlin">Berlin, Germany</option>
                            <option value="London">London, UK</option>
                            <option value="Los Angeles">Los Angeles, USA</option>
                            <option value="New York City">New York City, USA</option>
                            <option value="Paris">Paris, France</option>
                            <option value="Amsterdam">Amsterdam, Netherlands</option>
                          </select>
                        </div>
                        <div>
                          <label className="font-bold text-white/50 uppercase tracking-wider block mb-1">
                            Target Subgenre
                          </label>
                          <select
                            value={targetGenre}
                            onChange={(e) => dispatch(setTargetGenre(e.target.value))}
                            className="w-full bg-black/60 border border-white/10 rounded-lg p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
                          >
                            <option value="Techno">Industrial / Melodic Techno</option>
                            <option value="House">Deep House / Nu-Disco</option>
                            <option value="Ambient">Ambient & Neo-Classical</option>
                            <option value="Drum and Bass">Drum and Bass / Liquid</option>
                          </select>
                        </div>
                      </div>

                      {/* Dropzone */}
                      <div className="border-2 border-dashed border-white/10 hover:border-[#1DB954]/50 rounded-xl p-4 text-center cursor-pointer transition-colors bg-black/30">
                        <UploadCloud className="w-6 h-6 mx-auto text-[#1DB954] mb-1" />
                        <div className="font-bold text-white">Drag & drop raw demo .WAV or .MP3</div>
                        <div className="text-[10px] text-white/40 mt-0.5">32 Log-Mel Bands & Fourier Tempogram Extraction</div>
                      </div>

                      <button
                        onClick={runStudioDiagnostic}
                        disabled={isDiagnosing}
                        className="w-full mt-2 py-3 bg-[#1DB954] hover:bg-[#1ed760] text-black font-extrabold rounded-full text-sm transition-transform active:scale-95 shadow-lg shadow-[#1DB954]/20 flex items-center justify-center gap-2"
                      >
                        <Sparkles className="w-4 h-4" />
                        {isDiagnosing
                          ? "Extracting Mel-Tempograms..."
                          : "Run AI Diagnostic & Benchmark Sound"}
                      </button>
                    </div>
                  </div>

                  {/* Right: 3D Visualizer & Stem Mixer */}
                  <div className="bg-[#181818] rounded-2xl p-6 border border-white/[0.06] flex flex-col justify-between shadow-xl">
                    <div className="flex justify-between items-center pb-3 border-b border-white/10 mb-3">
                      <div className="font-bold text-white text-sm flex items-center gap-2">
                        <Disc3 className="w-4 h-4 text-[#1DB954]" /> Real-Time 3D Acoustic Pulse
                      </div>
                      <span className="text-xs font-mono font-bold text-[#1DB954]">
                        {currentTrack.bpm} BPM
                      </span>
                    </div>

                    <AudioVisualizer3D
                      bpm={currentTrack.bpm}
                      genre={currentTrack.genre}
                      isPlaying={isPlaying}
                    />

                    {/* Stem Mixer Desk */}
                    <div className="mt-4 pt-3 border-t border-white/10 space-y-2">
                      <div className="font-bold text-xs text-white/60 uppercase tracking-wider">
                        Virtual 4-Stem Acoustic Mixer
                      </div>
                      <div className="grid grid-cols-4 gap-2 text-[10px] font-mono">
                        {Object.entries(stems).map(([stemName, val]) => (
                          <div key={stemName} className="bg-black/50 p-2 rounded-lg border border-white/5 text-center">
                            <div className="text-white/50 uppercase font-bold">{stemName}</div>
                            <div className="text-[#1DB954] font-bold my-1">{val}%</div>
                            <input
                              type="range"
                              min="0"
                              max="100"
                              value={val}
                              onChange={(e) =>
                                setStems((prev) => ({
                                  ...prev,
                                  [stemName]: Number(e.target.value),
                                }))
                              }
                              className="w-full h-1 accent-[#1DB954] cursor-pointer"
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* 4-Phase Roadmap & Booking Pitch */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Interactive Checklist Roadmap */}
                  <div className="bg-[#181818] rounded-2xl p-6 border border-white/[0.06] space-y-3 shadow-xl">
                    <div className="font-bold text-white text-sm pb-2 border-b border-white/10 flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <Compass className="w-4 h-4 text-[#1DB954]" /> 4-Phase Zero-Debt Roadmap
                      </span>
                      <span className="text-[10px] font-mono text-[#1DB954] bg-[#1DB954]/10 px-2 py-0.5 rounded">
                        Interactive Checklist
                      </span>
                    </div>

                    <div className="space-y-2.5 text-xs">
                      {[
                        {
                          id: "step_0",
                          title: "Phase 1: Zero-Debt Calibration & Direct-to-Fan",
                          desc: "Calibrate tempo to 132 BPM. Master 3-track EP. Distribute lossless files via Bandcamp + DistroKid.",
                        },
                        {
                          id: "step_1",
                          title: "Phase 2: Gateway Curation & Rights Verification",
                          desc: "Submit stems to COLORS and HATE. Register with GEMA / SoundExchange prior to public release.",
                        },
                        {
                          id: "step_2",
                          title: "Phase 3: Showcase Circuits & A&R Scouts",
                          desc: "Apply for showcase slots at Reeperbahn Festival / ESNS to perform for international bookers.",
                        },
                        {
                          id: "step_3",
                          title: "Phase 4: Boutique Label Leverage",
                          desc: "Retain 100% publishing ownership. Negotiate single-EP licensing deal with a maximum 3-year term.",
                        },
                      ].map((step) => {
                        const isDone = completedRoadmapSteps[step.id];
                        return (
                          <div
                            key={step.id}
                            onClick={() => toggleRoadmapStep(step.id)}
                            className={`p-3 rounded-xl border cursor-pointer transition-all flex items-start gap-3 ${
                              isDone
                                ? "bg-[#1DB954]/10 border-[#1DB954]/40 text-white"
                                : "bg-black/40 border-white/5 hover:border-white/20 text-[#b3b3b3]"
                            }`}
                          >
                            <div className="mt-0.5">
                              {isDone ? (
                                <CheckSquare className="w-4 h-4 text-[#1DB954]" />
                              ) : (
                                <Square className="w-4 h-4 text-white/40" />
                              )}
                            </div>
                            <div className="flex-1">
                              <div
                                className={`font-bold ${
                                  isDone ? "text-[#1DB954] line-through" : "text-white"
                                }`}
                              >
                                {step.title}
                              </div>
                              <div className="text-white/60 mt-0.5 leading-relaxed">
                                {step.desc}
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Promoter Pitch Email */}
                  <div className="bg-[#181818] rounded-2xl p-6 border border-white/[0.06] space-y-3 shadow-xl">
                    <div className="flex justify-between items-center pb-2 border-b border-white/10">
                      <div className="font-bold text-white text-sm flex items-center gap-2">
                        <Send className="w-4 h-4 text-[#1DB954]" /> Automated Promoter Pitch Email
                      </div>
                      <button
                        onClick={copyPitch}
                        className="text-xs bg-white/10 hover:bg-white/20 text-white px-3 py-1 rounded-full font-semibold flex items-center gap-1 transition-all"
                      >
                        {copiedPitch ? (
                          <CheckCircle2 className="w-3.5 h-3.5 text-[#1DB954]" />
                        ) : (
                          <Copy className="w-3.5 h-3.5" />
                        )}
                        {copiedPitch ? "Copied!" : "Copy Pitch"}
                      </button>
                    </div>
                    <pre className="p-3.5 bg-black/60 border border-white/10 rounded-xl text-[11px] font-mono text-[#1DB954] whitespace-pre-wrap max-h-56 overflow-y-auto leading-relaxed">
                      {pitchText}
                    </pre>
                  </div>
                </div>
              </div>
            )}

            {/* ---------------------------------------------------- */}
            {/* VIEW 3: VENUES & PROMOTER PORTAL                     */}
            {/* ---------------------------------------------------- */}
            {activeNav === "venues" && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-[#181818] rounded-2xl p-6 border border-white/[0.06] space-y-4 shadow-xl">
                  <div className="font-bold text-white text-sm pb-2 border-b border-white/10 flex justify-between items-center">
                    <span>🏟️ Stepping-Stone Venue Directory</span>
                    <span className="text-xs text-white/40">Select a venue to book</span>
                  </div>
                  <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
                    {venuesList.map((v: VenueItem, idx: number) => (
                      <div
                        key={idx}
                        onClick={() => dispatch(setSelectedVenue(v))}
                        className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                          selectedVenue.name === v.name
                            ? "bg-white/10 border-[#1DB954] text-white shadow-lg"
                            : "bg-black/40 border-white/5 hover:border-white/20 text-[#b3b3b3]"
                        }`}
                      >
                        <div className="flex justify-between items-center">
                          <div className="font-bold text-sm text-white">{v.name}</div>
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-white font-bold">
                            {v.tier}
                          </span>
                        </div>
                        <div className="text-xs text-[#b3b3b3] mt-1">
                          {v.city} • Cap: {v.cap} • {v.sound}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-[#181818] rounded-2xl p-6 border border-white/[0.06] space-y-4 shadow-xl">
                  <div className="flex justify-between items-center pb-2 border-b border-white/10">
                    <div className="font-bold text-white text-sm">
                      Lineup Matchmaker & Formal Offer
                    </div>
                    <span className="text-xs font-mono text-[#1DB954] bg-[#1DB954]/10 px-2.5 py-1 rounded-full">
                      {selectedVenue.name}
                    </span>
                  </div>

                  <div className="space-y-3 text-xs">
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="font-bold text-white/50 uppercase block mb-1">
                          Offer Fee (EUR)
                        </label>
                        <input
                          type="number"
                          value={inquiryFee}
                          onChange={(e) => dispatch(setInquiryFee(e.target.value))}
                          className="w-full bg-black/60 border border-white/10 rounded-lg p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="font-bold text-white/50 uppercase block mb-1">
                          Performance Date
                        </label>
                        <input
                          type="date"
                          value={inquiryDate}
                          onChange={(e) => dispatch(setInquiryDate(e.target.value))}
                          className="w-full bg-black/60 border border-white/10 rounded-lg p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
                        />
                      </div>
                    </div>

                    <div className="flex gap-2 pt-2">
                      <button
                        onClick={dispatchBooking}
                        className="flex-1 py-3 bg-[#1DB954] hover:bg-[#1ed760] text-black font-extrabold rounded-full text-sm transition-transform active:scale-95 shadow-lg shadow-[#1DB954]/20"
                      >
                        📨 Dispatch Offer to Agent
                      </button>
                      <button
                        onClick={() => setShowContractModal(true)}
                        className="px-4 py-3 bg-white/10 hover:bg-white/20 text-white font-bold rounded-full text-xs transition-all flex items-center gap-1.5"
                      >
                        <FileText className="w-4 h-4" /> Preview Contract
                      </button>
                    </div>

                    {inquiryReceipt && (
                      <div className="p-3 bg-[#1DB954]/10 border border-[#1DB954]/30 rounded-xl text-xs text-[#1DB954] font-mono leading-relaxed">
                        {inquiryReceipt}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* ---------------------------------------------------- */}
            {/* VIEW 4: 3D GALAXY NETWORK                            */}
            {/* ---------------------------------------------------- */}
            {activeNav === "galaxy" && (
              <div className="space-y-4">
                <NetworkGraph3D />
              </div>
            )}

            {/* ---------------------------------------------------- */}
            {/* VIEW 5: GRAPHIFY MEMORY CHAT                         */}
            {/* ---------------------------------------------------- */}
            {activeNav === "memory" && (
              <div className="bg-[#181818] rounded-2xl p-6 border border-white/[0.06] flex flex-col h-[520px] shadow-xl">
                <div className="flex justify-between items-center pb-3 border-b border-white/10 mb-3">
                  <div className="font-bold text-white text-sm flex items-center gap-2">
                    <Brain className="w-4 h-4 text-[#1DB954]" /> Graphify Associative Recall Chat
                  </div>
                  <span className="text-xs font-mono text-[#1DB954] bg-[#1DB954]/10 px-2.5 py-0.5 rounded-full">
                    {isRecalling ? "Recalling..." : "Multi-Hop Memory Active"}
                  </span>
                </div>

                <div className="flex-1 overflow-y-auto space-y-3 p-3 bg-black/50 rounded-xl border border-white/5 mb-3">
                  {chatMessages.map((msg: any, idx: number) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-xl text-xs leading-relaxed max-w-[85%] ${
                        msg.sender === "user"
                          ? "ml-auto bg-[#1DB954] text-black font-semibold shadow-md"
                          : "mr-auto bg-[#242424] text-white border border-white/5"
                      }`}
                    >
                      {msg.text}
                    </div>
                  ))}
                </div>

                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Ask about publishing rights, synths, studios, or contracts..."
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSendChat()}
                    className="flex-1 bg-black/60 border border-white/10 rounded-full px-4 py-2.5 text-xs text-white focus:border-[#1DB954] focus:outline-none"
                  />
                  <button
                    onClick={handleSendChat}
                    className="px-5 bg-[#1DB954] hover:bg-[#1ed760] text-black font-bold rounded-full text-xs transition-all flex items-center gap-1.5"
                  >
                    <Send className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            )}

            {/* ---------------------------------------------------- */}
            {/* VIEW 6: INDUSTRY ANALYTICS                           */}
            {/* ---------------------------------------------------- */}
            {activeNav === "analytics" && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-[#181818] rounded-2xl p-6 border border-white/[0.06] space-y-4 shadow-xl">
                  <div className="font-bold text-white text-sm flex items-center gap-2 pb-2 border-b border-white/10">
                    <Globe2 className="w-4 h-4 text-[#1DB954]" /> De-Anglicization Index
                  </div>
                  <div className="text-center py-6">
                    <div className="text-5xl font-black text-[#1DB954] font-mono tracking-tight">
                      56.4%
                    </div>
                    <div className="text-xs text-[#b3b3b3] mt-2 font-medium">
                      Global Non-Anglo Music Dominance
                    </div>
                  </div>
                  <p className="text-xs text-white/40 leading-relaxed">
                    Mined across 11+ non-English and diaspora territories (Germany, South Korea, Nigeria, Jamaica, France, Japan, Brazil).
                  </p>
                </div>

                <div className="bg-[#181818] rounded-2xl p-6 border border-white/[0.06] space-y-4 shadow-xl">
                  <div className="font-bold text-white text-sm flex items-center gap-2 pb-2 border-b border-white/10">
                    <Sparkles className="w-4 h-4 text-purple-400" /> Breakout A&R Radar
                  </div>
                  <div className="space-y-2 text-xs">
                    {[
                      { name: "Aphex Twin", sub: "Ambient / IDM", score: "2.25" },
                      { name: "Nils Frahm", sub: "Neo-Classical", score: "2.25" },
                      { name: "Burna Boy", sub: "Afrobeats / Lagos", score: "1.94" },
                    ].map((a, idx) => (
                      <div
                        key={idx}
                        className="p-3 bg-black/40 rounded-xl flex justify-between items-center border border-white/5"
                      >
                        <div>
                          <div className="font-bold text-white">{a.name}</div>
                          <div className="text-[10px] text-[#b3b3b3]">{a.sub}</div>
                        </div>
                        <span className="font-mono text-[#1DB954] font-bold">
                          {a.score} VELOCITY
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-[#181818] rounded-2xl p-6 border border-white/[0.06] space-y-4 shadow-xl">
                  <div className="font-bold text-white text-sm flex items-center gap-2 pb-2 border-b border-white/10">
                    <Flame className="w-4 h-4 text-amber-400" /> Producer Export Hubs
                  </div>
                  <div className="space-y-2 text-xs">
                    {[
                      {
                        hub: "Sweden (Stockholm)",
                        producers: "Max Martin, Shellback",
                        export: "50.0%",
                      },
                      {
                        hub: "United States (LA / NYC)",
                        producers: "Dr. Dre, Rick Rubin",
                        export: "21.1%",
                      },
                      {
                        hub: "United Kingdom (London)",
                        producers: "Brian Eno, George Martin",
                        export: "14.3%",
                      },
                    ].map((h, idx) => (
                      <div
                        key={idx}
                        className="p-3 bg-black/40 rounded-xl flex justify-between items-center border border-white/5"
                      >
                        <div>
                          <div className="font-bold text-white">{h.hub}</div>
                          <div className="text-[10px] text-[#b3b3b3]">
                            {h.producers}
                          </div>
                        </div>
                        <span className="font-mono text-[#1DB954] font-bold">
                          {h.export}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>

        {/* ========================================================= */}
        {/* 3. SPOTIFY RIGHT DRAWER                                   */}
        {/* ========================================================= */}
        {showRightDrawer && (
          <aside className="w-72 bg-[#121212] rounded-xl p-4 flex flex-col gap-4 shrink-0 border border-white/[0.06] shadow-2xl overflow-y-auto text-xs">
            <div className="font-bold text-white text-sm pb-2 border-b border-white/10 flex justify-between items-center">
              <span>Track Intelligence</span>
              <span className="text-[10px] font-mono text-[#1DB954] bg-[#1DB954]/10 px-2 py-0.5 rounded font-bold">
                REDUX SYNC
              </span>
            </div>

            <div className="rounded-xl overflow-hidden bg-black/40 border border-white/10 aspect-video relative shadow-lg">
              <img
                src={currentTrack.cover}
                alt="Cover"
                className="w-full h-full object-cover"
              />
              <div className="absolute bottom-2 left-2 px-2 py-0.5 rounded bg-black/75 text-[10px] font-mono text-white">
                {currentTrack.bpm} BPM
              </div>
            </div>

            <div>
              <div className="font-bold text-white text-sm">
                {currentTrack.title}
              </div>
              <div className="text-[#b3b3b3]">{currentTrack.artist}</div>
            </div>

            <div className="p-3 bg-[#181818] rounded-xl border border-white/5 space-y-2">
              <div className="font-bold text-white">Acoustic Fingerprint</div>
              <div className="grid grid-cols-2 gap-2 text-[11px]">
                <div className="text-white/50">
                  Genre:{" "}
                  <span className="text-white font-medium">
                    {currentTrack.genre}
                  </span>
                </div>
                <div className="text-white/50">
                  Tempo:{" "}
                  <span className="text-[#1DB954] font-mono font-bold">
                    {currentTrack.bpm} BPM
                  </span>
                </div>
                <div className="text-white/50">
                  Mel Bands: <span className="text-white font-mono">32 Log</span>
                </div>
                <div className="text-white/50">
                  Tempogram: <span className="text-white font-mono">48 Bins</span>
                </div>
              </div>
            </div>

            <div className="p-3 bg-[#181818] rounded-xl border border-white/5 space-y-1.5">
              <div className="font-bold text-white">Master Rights & Credits</div>
              <div className="text-[11px] text-white/50">
                Studio: <span className="text-white">Funkhaus Studio 1</span>
              </div>
              <div className="text-[11px] text-white/50">
                Rights:{" "}
                <span className="text-[#1DB954] font-bold">100% Artist Owned</span>
              </div>
              <div className="text-[11px] text-white/50">
                Publishing: <span className="text-white">GEMA Registered</span>
              </div>
            </div>
          </aside>
        )}
      </div>

      {/* ========================================================= */}
      {/* 4. SPOTIFY BOTTOM NOW PLAYING BAR                          */}
      {/* ========================================================= */}
      <footer className="h-20 bg-black border-t border-white/10 px-6 flex items-center justify-between shrink-0 z-50">
        <div className="flex items-center gap-3.5 w-1/4 min-w-[200px]">
          <img
            src={currentTrack.cover}
            alt="Cover"
            className="w-13 h-13 rounded-lg object-cover shadow-lg border border-white/10"
          />
          <div className="truncate">
            <div className="text-xs font-bold text-white truncate hover:underline cursor-pointer">
              {currentTrack.title}
            </div>
            <div className="text-[11px] text-[#b3b3b3] truncate hover:underline cursor-pointer">
              {currentTrack.artist}
            </div>
          </div>
          <button
            onClick={() => dispatch(toggleLike())}
            className="text-white/60 hover:text-white ml-2 transition-colors"
          >
            <Heart
              className={`w-4 h-4 ${
                isLiked ? "fill-[#1DB954] text-[#1DB954]" : ""
              }`}
            />
          </button>
        </div>

        <div className="flex flex-col items-center gap-1.5 w-2/4 max-w-xl">
          <div className="flex items-center gap-5">
            <button className="text-white/60 hover:text-white transition-colors">
              <Shuffle className="w-4 h-4" />
            </button>
            <button className="text-white/60 hover:text-white transition-colors">
              <SkipBack className="w-4 h-4 fill-current" />
            </button>
            <button
              onClick={() => dispatch(togglePlay())}
              className="w-9 h-9 rounded-full bg-white hover:scale-105 flex items-center justify-center transition-transform shadow-xl"
            >
              {isPlaying ? (
                <Pause className="w-4 h-4 fill-black text-black" />
              ) : (
                <Play className="w-4 h-4 fill-black text-black ml-0.5" />
              )}
            </button>
            <button className="text-white/60 hover:text-white transition-colors">
              <SkipForward className="w-4 h-4 fill-current" />
            </button>
            <button className="text-white/60 hover:text-white transition-colors">
              <Repeat className="w-4 h-4" />
            </button>
          </div>

          <div className="w-full flex items-center gap-2 text-[10px] font-mono text-white/50">
            <span>
              {Math.floor(
                (currentTrack.progress / 100) *
                  (Number(currentTrack.duration.split(":")[0]) * 60 +
                    Number(currentTrack.duration.split(":")[1])) /
                  60
              )}
              :
              {String(
                Math.floor(
                  ((currentTrack.progress / 100) *
                    (Number(currentTrack.duration.split(":")[0]) * 60 +
                      Number(currentTrack.duration.split(":")[1]))) %
                    60
                )
              ).padStart(2, "0")}
            </span>
            <div
              onClick={(e) => {
                const rect = e.currentTarget.getBoundingClientRect();
                const clickX = e.clientX - rect.left;
                const newProgress = (clickX / rect.width) * 100;
                dispatch(setProgress(newProgress));
              }}
              className="flex-1 h-1 bg-white/20 rounded-full overflow-hidden cursor-pointer group hover:h-1.5 transition-all"
            >
              <div
                className="h-full bg-white group-hover:bg-[#1DB954] transition-colors"
                style={{ width: `${currentTrack.progress}%` }}
              ></div>
            </div>
            <span>{currentTrack.duration}</span>
          </div>
        </div>

        <div className="flex items-center justify-end gap-3 w-1/4 min-w-[200px]">
          <div className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-white/10 text-white font-bold">
            {currentTrack.bpm} BPM
          </div>
          <button
            onClick={() => dispatch(setVolume(volume === 0 ? 80 : 0))}
            className="text-white/60 hover:text-white transition-colors"
          >
            {volume === 0 ? (
              <VolumeX className="w-4 h-4" />
            ) : (
              <Volume2 className="w-4 h-4" />
            )}
          </button>
          <input
            type="range"
            min="0"
            max="100"
            value={volume}
            onChange={(e) => dispatch(setVolume(Number(e.target.value)))}
            className="w-20 h-1 accent-[#1DB954] cursor-pointer"
          />
        </div>
      </footer>

      {/* Contract Preview Modal */}
      {showContractModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="bg-[#181818] border border-white/10 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <div className="flex justify-between items-center pb-3 border-b border-white/10">
              <div className="font-bold text-white flex items-center gap-2">
                <FileText className="w-4 h-4 text-[#1DB954]" /> Standard Performance Engagement Contract
              </div>
              <button
                onClick={() => setShowContractModal(false)}
                className="text-white/60 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="text-xs text-slate-300 font-mono space-y-2 bg-black/60 p-4 rounded-xl max-h-60 overflow-y-auto">
              <div><b>ENGAGEMENT AGREEMENT</b></div>
              <div><b>Artist:</b> {artistName}</div>
              <div><b>Venue:</b> {selectedVenue.name} ({selectedVenue.city})</div>
              <div><b>Date:</b> {inquiryDate}</div>
              <div><b>Agreed Guaranteed Fee:</b> {inquiryFee} EUR Net</div>
              <div><b>Sound Rider:</b> {selectedVenue.sound}</div>
              <div><b>Soundcheck:</b> 17:00 CET | <b>Set Duration:</b> 90 minutes</div>
              <div><b>Master Rights:</b> 100% Retained by Artist (No Predatory Clauses).</div>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => {
                  setShowContractModal(false);
                  showToast("Contract PDF exported to downloads!");
                }}
                className="flex-1 py-2.5 bg-[#1DB954] hover:bg-[#1ed760] text-black font-extrabold rounded-full text-xs flex items-center justify-center gap-1.5"
              >
                <Download className="w-3.5 h-3.5" /> Download Contract PDF
              </button>
              <button
                onClick={() => setShowContractModal(false)}
                className="px-4 py-2.5 bg-white/10 hover:bg-white/20 text-white font-bold rounded-full text-xs"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
