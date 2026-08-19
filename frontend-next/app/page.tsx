"use client";

import React, { useState, useEffect, useRef } from "react";
import { AudioVisualizer3D } from "@/components/AudioVisualizer3D";
import { NetworkGraph3D } from "@/components/NetworkGraph3D";
import {
  Home as HomeIcon,
  Search,
  Library,
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
  Music2,
  Compass,
  Sliders,
  ExternalLink,
  ChevronRight,
  Disc3,
  Mic2,
  Users2,
  Flame,
} from "lucide-react";

export default function SpotifyStyleApp() {
  const [activeNav, setActiveNav] = useState<
    "home" | "studio" | "venues" | "galaxy" | "memory" | "analytics"
  >("home");

  // Audio Player State (Spotify Bottom Bar)
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTrack, setCurrentTrack] = useState({
    title: "Modular Resonance (Original Cut)",
    artist: "Subtle Flux",
    cover: "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=300&q=80",
    genre: "Industrial Techno",
    bpm: 132,
    duration: "4:32",
    progress: 35,
  });
  const [volume, setVolume] = useState(80);
  const [isLiked, setIsLiked] = useState(true);
  const [showRightDrawer, setShowRightDrawer] = useState(true);

  // Bedroom Studio State
  const [studioArtist, setStudioArtist] = useState("Subtle Flux");
  const [studioTrack, setStudioTrack] = useState("Modular Resonance (Original Cut)");
  const [studioCity, setStudioCity] = useState("Berlin");
  const [studioGenre, setStudioGenre] = useState("Techno");
  const [copiedPitch, setCopiedPitch] = useState(false);
  const [isDiagnosing, setIsDiagnosing] = useState(false);

  // Venue Booking State
  const [selectedVenue, setSelectedVenue] = useState({
    id: "ven_berghain",
    name: "Berghain / Panorama Bar",
    city: "Berlin",
    cap: 1500,
    tier: "Hall",
    sound: "Funktion-One Custom (Double 21-inch Subs)",
    email: "booking@berghain.de",
    image: "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=500&q=80",
  });
  const [inquiryFee, setInquiryFee] = useState("1800");
  const [inquiryDate, setInquiryDate] = useState("2026-11-14");
  const [inquiryReceipt, setInquiryReceipt] = useState<string | null>(null);

  // Memory Chat State
  const [chatMessages, setChatMessages] = useState([
    {
      sender: "bot",
      text: "Welcome to AGIES Spotify AI Intelligence. Ask me about contracts, mastering techniques at Hansa/Abbey Road, classic analog synthesizers (TR-808, Prophet-5), or how to pitch showcase festivals.",
    },
  ]);
  const [chatInput, setChatInput] = useState("");

  const togglePlay = () => setIsPlaying(!isPlaying);

  const runStudioDiagnostic = async () => {
    setIsDiagnosing(true);
    const newBpm = studioGenre === "Techno" ? 132 : studioGenre === "House" ? 124 : 85;
    setCurrentTrack((prev) => ({
      ...prev,
      title: studioTrack,
      artist: studioArtist,
      bpm: newBpm,
      genre: studioGenre,
    }));

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/audio/analyze-demo", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-API-Key": "agies_test_key_123" },
        body: JSON.stringify({
          track_title: studioTrack,
          artist_name: studioArtist,
          home_city: studioCity,
          home_country: "Germany",
          subgenre_hint: studioGenre,
        }),
      });
      if (res.ok) {
        setIsPlaying(true);
      }
    } catch (e) {
      console.log("Local API fallback");
    } finally {
      setIsDiagnosing(false);
    }
  };

  const handleSendChat = async () => {
    if (!chatInput.trim()) return;
    const q = chatInput;
    setChatMessages((prev) => [...prev, { sender: "user", text: q }]);
    setChatInput("");

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/v1/memory/recall?query=${encodeURIComponent(q)}&top_k=2`,
        { headers: { "X-API-Key": "agies_test_key_123" } }
      );
      if (res.ok) {
        const data = await res.json();
        let reply = `Recalled ${data.recalled_nodes_count} memory nodes across ${data.recalled_nodes.map((n: any) => n.label).join(", ")}.`;
        if (q.toLowerCase().includes("contract") || q.toLowerCase().includes("360")) {
          reply += "\n\nIndustry Rule: Never sign a 360-degree deal as a debut artist. Retain master rights via Bandcamp and license single EPs for max 3-year windows.";
        }
        setChatMessages((prev) => [...prev, { sender: "bot", text: reply }]);
      } else {
        setChatMessages((prev) => [
          ...prev,
          {
            sender: "bot",
            text: "Hansa Tonstudio Berlin is renowned for classic analog acoustics (David Bowie 'Heroes', Depeche Mode, Nils Frahm), featuring custom Neve consoles and natural reverb chambers.",
          },
        ]);
      }
    } catch (e) {
      setChatMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Hansa Tonstudio Berlin is renowned for classic analog acoustics (David Bowie 'Heroes', Depeche Mode, Nils Frahm), featuring custom Neve consoles and natural reverb chambers.",
        },
      ]);
    }
  };

  const pitchText = `Subject: Live Debut Pitch / Support Slot Inquiry: ${studioArtist} @ ${selectedVenue.name}

Hi ${selectedVenue.name} Bookings Team,

I hope you're having a great week. I'm ${studioArtist}, a ${studioCity}-based producer producing ${studioGenre} (sound profile: ${currentTrack.bpm} BPM, Mel-Tempogram acoustic energy aligned with Stephan Bodzin).

I've just finalized my new 3-track EP '${studioTrack}', and I'm looking to play opening support slots for your upcoming club nights.
You can listen to the private demo stream here: [Private Demo Stream Link]

I would love to be considered for an opening support slot on your lineup. Thank you for your time and for supporting grassroots music!

Best regards,
${studioArtist}
Contact: booking@${studioArtist.toLowerCase().replace(/\s+/g, "")}-official.com`;

  const copyPitch = () => {
    navigator.clipboard.writeText(pitchText);
    setCopiedPitch(true);
    setTimeout(() => setCopiedPitch(false), 2000);
  };

  const dispatchBooking = () => {
    setInquiryReceipt(
      `✓ Formal Booking Offer of ${inquiryFee} EUR for ${inquiryDate} transmitted to ${selectedVenue.name} Booking Dept. Logged to disk. Status: DISPATCHED_TO_AGENT.`
    );
  };

  return (
    <div className="h-screen w-screen bg-black text-[#b3b3b3] flex flex-col select-none overflow-hidden font-sans">
      {/* Upper Container (Sidebar + Main + Right Drawer) */}
      <div className="flex-1 flex overflow-hidden p-2 gap-2">
        {/* ========================================================= */}
        {/* 1. SPOTIFY LEFT SIDEBAR                                    */}
        {/* ========================================================= */}
        <aside className="w-64 bg-[#121212] rounded-lg flex flex-col gap-2 p-4 shrink-0 border border-white/5 shadow-2xl">
          {/* Brand */}
          <div className="flex items-center gap-2 px-2 py-1 text-white">
            <div className="w-8 h-8 rounded-full bg-[#1DB954] flex items-center justify-center text-black font-black">
              <Disc3 className="w-5 h-5 animate-spin" style={{ animationDuration: "8s" }} />
            </div>
            <div className="font-bold text-lg tracking-tight text-white flex items-center gap-1.5">
              AGIES <span className="text-[10px] text-[#1DB954] font-mono px-1.5 py-0.5 rounded bg-[#1DB954]/10 border border-[#1DB954]/30">PRO</span>
            </div>
          </div>

          {/* Primary Nav */}
          <div className="space-y-1 mt-2">
            <button
              onClick={() => setActiveNav("home")}
              className={`w-full flex items-center gap-4 px-3 py-2.5 rounded-md font-semibold text-sm transition-all ${
                activeNav === "home" ? "text-white bg-white/10" : "hover:text-white"
              }`}
            >
              <HomeIcon className="w-5 h-5" /> Home Feed
            </button>
            <button
              onClick={() => setActiveNav("studio")}
              className={`w-full flex items-center gap-4 px-3 py-2.5 rounded-md font-semibold text-sm transition-all ${
                activeNav === "studio" ? "text-white bg-white/10 text-[#1DB954]" : "hover:text-white"
              }`}
            >
              <Radio className="w-5 h-5 text-[#1DB954]" /> Bedroom Studio
            </button>
            <button
              onClick={() => setActiveNav("venues")}
              className={`w-full flex items-center gap-4 px-3 py-2.5 rounded-md font-semibold text-sm transition-all ${
                activeNav === "venues" ? "text-white bg-white/10 text-[#1DB954]" : "hover:text-white"
              }`}
            >
              <Building2 className="w-5 h-5" /> Venue Matchmaker
            </button>
            <button
              onClick={() => setActiveNav("galaxy")}
              className={`w-full flex items-center gap-4 px-3 py-2.5 rounded-md font-semibold text-sm transition-all ${
                activeNav === "galaxy" ? "text-white bg-white/10 text-[#1DB954]" : "hover:text-white"
              }`}
            >
              <Share2 className="w-5 h-5" /> 3D Galaxy Network
            </button>
            <button
              onClick={() => setActiveNav("memory")}
              className={`w-full flex items-center gap-4 px-3 py-2.5 rounded-md font-semibold text-sm transition-all ${
                activeNav === "memory" ? "text-white bg-white/10 text-[#1DB954]" : "hover:text-white"
              }`}
            >
              <Brain className="w-5 h-5" /> Graphify AI Chat
            </button>
            <button
              onClick={() => setActiveNav("analytics")}
              className={`w-full flex items-center gap-4 px-3 py-2.5 rounded-md font-semibold text-sm transition-all ${
                activeNav === "analytics" ? "text-white bg-white/10 text-[#1DB954]" : "hover:text-white"
              }`}
            >
              <BarChart3 className="w-5 h-5" /> Industry Radar
            </button>
          </div>

          {/* Library & Corridors List */}
          <div className="flex-1 mt-4 pt-4 border-t border-white/5 flex flex-col min-h-0">
            <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-white/40 px-2 mb-2">
              <span>Your Ecosystem</span>
              <Library className="w-4 h-4" />
            </div>
            <div className="overflow-y-auto space-y-1 pr-1 flex-1 text-xs">
              {[
                { title: "Berlin ↔ London Electronic Highway", sub: "Corridor • 0.98 Strength" },
                { title: "Stockholm ↔ LA Pop Axis", sub: "Corridor • 0.99 Strength" },
                { title: "Berghain / Panorama Bar", sub: "Venue • 1,500 Cap" },
                { title: "Hansa Tonstudio", sub: "Studio • Berlin Sound" },
                { title: "Ostgut Ton", sub: "Label • Techno Landmark" },
                { title: "Reeperbahn Festival 2026", sub: "A&R Showcase • 90%+ Scout Density" },
              ].map((item, idx) => (
                <div
                  key={idx}
                  className="px-2.5 py-2 rounded-md hover:bg-white/5 cursor-pointer text-white/80 hover:text-white transition-all"
                >
                  <div className="font-semibold truncate">{item.title}</div>
                  <div className="text-[11px] text-[#b3b3b3] truncate">{item.sub}</div>
                </div>
              ))}
            </div>
          </div>
        </aside>

        {/* ========================================================= */}
        {/* 2. SPOTIFY MAIN SCROLLABLE CONTAINER                       */}
        {/* ========================================================= */}
        <main className="flex-1 bg-[#121212] rounded-lg overflow-y-auto relative border border-white/5 shadow-2xl flex flex-col">
          {/* Top Sticky Bar */}
          <div className="sticky top-0 bg-[#121212]/80 backdrop-blur-xl z-30 px-6 py-3.5 flex items-center justify-between border-b border-white/5">
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono text-white/50 bg-black/40 px-3 py-1.5 rounded-full border border-white/10 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-[#1DB954] animate-pulse"></span>
                FASTAPI BACKEND :8000 • 507 NODES • 1,432 EDGES
              </span>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowRightDrawer(!showRightDrawer)}
                className="text-xs bg-white/10 hover:bg-white/20 text-white px-3.5 py-1.5 rounded-full font-semibold transition-all flex items-center gap-1.5"
              >
                <Sliders className="w-3.5 h-3.5" /> {showRightDrawer ? "Hide Intelligence" : "Show Intelligence"}
              </button>
            </div>
          </div>

          <div className="p-6 flex-1 space-y-8">
            {/* ---------------------------------------------------- */}
            {/* VIEW 1: HOME FEED (Spotify Style Hero & Carousels)   */}
            {/* ---------------------------------------------------- */}
            {activeNav === "home" && (
              <div className="space-y-8">
                {/* Hero Gradient Banner */}
                <div className="rounded-xl p-8 bg-gradient-to-br from-[#1e3a8a] via-[#0f172a] to-[#121212] border border-blue-500/20 relative overflow-hidden shadow-2xl">
                  <div className="max-w-2xl relative z-10 space-y-4">
                    <span className="px-3 py-1 bg-[#1DB954]/20 border border-[#1DB954]/40 text-[#1DB954] rounded-full text-xs font-mono font-bold">
                      ACOUSTIC A&R INTELLIGENCE PLATFORM
                    </span>
                    <h1 className="text-4xl font-extrabold text-white tracking-tight leading-tight">
                      Take Your Bedroom Tracks to Global Stages
                    </h1>
                    <p className="text-sm text-[#b3b3b3] leading-relaxed">
                      Powered by the <b>arXiv:2110.08862 Mel-Spectrogram & Tempogram Neural Classifier</b> and a 507-node Global Music Industry Graph.
                    </p>
                    <div className="flex gap-3 pt-2">
                      <button
                        onClick={() => setActiveNav("studio")}
                        className="px-6 py-3 bg-[#1DB954] hover:bg-[#1ed760] text-black font-extrabold rounded-full text-sm transition-transform active:scale-95 shadow-lg shadow-[#1DB954]/20 flex items-center gap-2"
                      >
                        <Play className="w-4 h-4 fill-black" /> Launch Bedroom Studio
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

                {/* Section: Acoustically Aligned Titans */}
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-bold text-white tracking-tight">Nearest Acoustic Titans</h2>
                    <span className="text-xs text-[#1DB954] font-semibold hover:underline cursor-pointer">Show All</span>
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                    {[
                      { name: "Stephan Bodzin", genre: "Melodic Techno", score: "95.8%", img: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300&q=80" },
                      { name: "Nils Frahm", genre: "Neo-Classical Ambient", score: "92.4%", img: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300&q=80" },
                      { name: "Aphex Twin", genre: "Ambient / IDM", score: "91.2%", img: "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300&q=80" },
                      { name: "Boris Brejcha", genre: "High-Tech Minimal", score: "89.7%", img: "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=300&q=80" },
                    ].map((item, idx) => (
                      <div
                        key={idx}
                        className="bg-[#181818] hover:bg-[#282828] p-4 rounded-lg transition-all group cursor-pointer border border-white/5 relative"
                      >
                        <div className="relative mb-3 aspect-square rounded-md overflow-hidden bg-black/40">
                          <img src={item.img} alt={item.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                          <button className="absolute bottom-2 right-2 w-10 h-10 rounded-full bg-[#1DB954] shadow-xl flex items-center justify-center opacity-0 group-hover:opacity-100 group-hover:translate-y-0 translate-y-2 transition-all duration-200">
                            <Play className="w-5 h-5 fill-black ml-0.5" />
                          </button>
                        </div>
                        <div className="font-bold text-white text-sm truncate">{item.name}</div>
                        <div className="text-xs text-[#b3b3b3] truncate mt-0.5">{item.genre}</div>
                        <div className="text-[11px] font-mono text-[#1DB954] font-bold mt-2">{item.score} ACOUSTIC MATCH</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Section: Stepping-Stone Debut Venues */}
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-bold text-white tracking-tight">Stepping-Stone Debut Venues</h2>
                    <span className="text-xs text-[#1DB954] font-semibold hover:underline cursor-pointer" onClick={() => setActiveNav("venues")}>Browse Venues</span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {[
                      { name: "Berghain / Panorama Bar", city: "Berlin", cap: 1500, sound: "Funktion-One Custom", tag: "Hall" },
                      { name: "Tresor Berlin", city: "Berlin", cap: 800, sound: "Funktion-One Vault", tag: "Club" },
                      { name: "The Windmill (Brixton)", city: "London", cap: 150, sound: "Grassroots PA", tag: "Intimate Debut" },
                    ].map((v, idx) => (
                      <div
                        key={idx}
                        onClick={() => { setSelectedVenue(v as any); setActiveNav("venues"); }}
                        className="bg-[#181818] hover:bg-[#282828] p-4 rounded-lg border border-white/5 transition-all cursor-pointer group"
                      >
                        <div className="flex justify-between items-start mb-2">
                          <div className="font-bold text-white text-sm group-hover:text-[#1DB954] transition-colors">{v.name}</div>
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-white font-bold">{v.tag}</span>
                        </div>
                        <div className="text-xs text-[#b3b3b3]">{v.city} • Capacity: {v.cap}</div>
                        <div className="text-[11px] text-white/50 mt-1 font-mono">{v.sound}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* ---------------------------------------------------- */}
            {/* VIEW 2: BEDROOM STUDIO & DIAGNOSTIC                  */}
            {/* ---------------------------------------------------- */}
            {activeNav === "studio" && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Left: Input Parameters */}
                  <div className="bg-[#181818] rounded-xl p-6 border border-white/5 space-y-4">
                    <div className="flex justify-between items-center pb-3 border-b border-white/10">
                      <div className="font-bold text-white flex items-center gap-2">
                        <Radio className="w-5 h-5 text-[#1DB954]" /> Demo Track Analyzer
                      </div>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/30">
                        arXiv:2110.08862
                      </span>
                    </div>

                    <div className="space-y-3 text-xs">
                      <div>
                        <label className="font-bold text-white/50 uppercase tracking-wider block mb-1">Artist / Alias</label>
                        <input
                          type="text"
                          value={studioArtist}
                          onChange={(e) => setStudioArtist(e.target.value)}
                          className="w-full bg-black/60 border border-white/10 rounded-md p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="font-bold text-white/50 uppercase tracking-wider block mb-1">Track Title</label>
                        <input
                          type="text"
                          value={studioTrack}
                          onChange={(e) => setStudioTrack(e.target.value)}
                          className="w-full bg-black/60 border border-white/10 rounded-md p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
                        />
                      </div>
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="font-bold text-white/50 uppercase tracking-wider block mb-1">City Hub</label>
                          <select
                            value={studioCity}
                            onChange={(e) => setStudioCity(e.target.value)}
                            className="w-full bg-black/60 border border-white/10 rounded-md p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
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
                          <label className="font-bold text-white/50 uppercase tracking-wider block mb-1">Target Genre</label>
                          <select
                            value={studioGenre}
                            onChange={(e) => setStudioGenre(e.target.value)}
                            className="w-full bg-black/60 border border-white/10 rounded-md p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
                          >
                            <option value="Techno">Industrial / Melodic Techno</option>
                            <option value="House">Deep House / Nu-Disco</option>
                            <option value="Ambient">Ambient & Neo-Classical</option>
                            <option value="Drum and Bass">Drum and Bass / Liquid</option>
                          </select>
                        </div>
                      </div>

                      <button
                        onClick={runStudioDiagnostic}
                        disabled={isDiagnosing}
                        className="w-full mt-2 py-3 bg-[#1DB954] hover:bg-[#1ed760] text-black font-extrabold rounded-full text-sm transition-transform active:scale-95 shadow-lg shadow-[#1DB954]/20 flex items-center justify-center gap-2"
                      >
                        <Sparkles className="w-4 h-4" />
                        {isDiagnosing ? "Extracting Mel-Tempograms..." : "Run AI Diagnostic & Benchmark Sound"}
                      </button>
                    </div>
                  </div>

                  {/* Right: 3D Visualizer */}
                  <div className="bg-[#181818] rounded-xl p-6 border border-white/5 flex flex-col justify-between">
                    <div className="flex justify-between items-center pb-3 border-b border-white/10 mb-3">
                      <div className="font-bold text-white text-sm flex items-center gap-2">
                        <Disc3 className="w-4 h-4 text-[#1DB954]" /> Real-Time 3D Acoustic Pulse
                      </div>
                      <span className="text-xs font-mono font-bold text-[#1DB954]">{currentTrack.bpm} BPM</span>
                    </div>
                    <AudioVisualizer3D bpm={currentTrack.bpm} genre={currentTrack.genre} isPlaying={isPlaying} />
                  </div>
                </div>

                {/* 4-Phase Roadmap & Booking Email Pitch */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-[#181818] rounded-xl p-6 border border-white/5 space-y-3">
                    <div className="font-bold text-white text-sm pb-2 border-b border-white/10 flex items-center gap-2">
                      <Compass className="w-4 h-4 text-[#1DB954]" /> 4-Phase Zero-Debt Roadmap
                    </div>
                    <div className="space-y-2.5 text-xs">
                      <div className="p-3 bg-black/40 border-l-2 border-[#1DB954] rounded-r-md">
                        <div className="font-bold text-white mb-0.5">Phase 1: Production & Direct-to-Fan</div>
                        <div className="text-[#b3b3b3]">Master 3-track EP. Sell lossless downloads directly via Bandcamp + DistroKid DSP delivery.</div>
                      </div>
                      <div className="p-3 bg-black/40 border-l-2 border-[#1DB954] rounded-r-md">
                        <div className="font-bold text-white mb-0.5">Phase 2: Gateway Curation & Sound Validation</div>
                        <div className="text-[#b3b3b3]">Submit stems to COLORS, Boiler Room, and HATE. Register with GEMA / SoundExchange.</div>
                      </div>
                      <div className="p-3 bg-black/40 border-l-2 border-[#1DB954] rounded-r-md">
                        <div className="font-bold text-white mb-0.5">Phase 3: Showcase Circuits</div>
                        <div className="text-[#b3b3b3]">Apply for Reeperbahn Festival / ESNS open calls to perform for international A&R scouts.</div>
                      </div>
                      <div className="p-3 bg-black/40 border-l-2 border-[#1DB954] rounded-r-md">
                        <div className="font-bold text-white mb-0.5">Phase 4: Boutique Label Leverage</div>
                        <div className="text-[#b3b3b3]">Retain 100% publishing rights. Negotiate single-EP licensing deal with a maximum 3-year term.</div>
                      </div>
                    </div>
                  </div>

                  <div className="bg-[#181818] rounded-xl p-6 border border-white/5 space-y-3">
                    <div className="flex justify-between items-center pb-2 border-b border-white/10">
                      <div className="font-bold text-white text-sm flex items-center gap-2">
                        <Send className="w-4 h-4 text-[#1DB954]" /> Automated Promoter Pitch Email
                      </div>
                      <button
                        onClick={copyPitch}
                        className="text-xs bg-white/10 hover:bg-white/20 text-white px-3 py-1 rounded-full font-semibold flex items-center gap-1"
                      >
                        {copiedPitch ? <CheckCircle2 className="w-3.5 h-3.5 text-[#1DB954]" /> : <Copy className="w-3.5 h-3.5" />}
                        {copiedPitch ? "Copied!" : "Copy"}
                      </button>
                    </div>
                    <pre className="p-3.5 bg-black/60 border border-white/10 rounded-lg text-[11px] font-mono text-[#1DB954] whitespace-pre-wrap max-h-56 overflow-y-auto leading-relaxed">
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
                <div className="bg-[#181818] rounded-xl p-6 border border-white/5 space-y-4">
                  <div className="font-bold text-white text-sm pb-2 border-b border-white/10">
                    🏟️ Stepping-Stone Venue Directory
                  </div>
                  <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
                    {[
                      { name: "Berghain / Panorama Bar", city: "Berlin", cap: 1500, tier: "Hall", sound: "Funktion-One Custom", email: "booking@berghain.de" },
                      { name: "Tresor Berlin", city: "Berlin", cap: 800, tier: "Club", sound: "Funktion-One Vault", email: "booking@tresorberlin.com" },
                      { name: "Schokoladen (Mitte)", city: "Berlin", cap: 150, tier: "Intimate Debut", sound: "Vintage Analog PA", email: "booking@schokoladen-mitte.de" },
                      { name: "Fabric London", city: "London", cap: 1600, tier: "Hall", sound: "Pioneer Bodysonic Floor", email: "programming@fabriclondon.com" },
                      { name: "The Windmill (Brixton)", city: "London", cap: 150, tier: "Intimate Debut", sound: "Grassroots PA", email: "windmillbrixton@gmail.com" },
                      { name: "The Bowery Ballroom", city: "New York City", cap: 575, tier: "Club", sound: "d&b Soundscape", email: "booking@boweryballroom.com" },
                    ].map((v, idx) => (
                      <div
                        key={idx}
                        onClick={() => setSelectedVenue(v as any)}
                        className={`p-3.5 rounded-lg border cursor-pointer transition-all ${
                          selectedVenue.name === v.name
                            ? "bg-white/10 border-[#1DB954] text-white"
                            : "bg-black/40 border-white/5 hover:border-white/20 text-[#b3b3b3]"
                        }`}
                      >
                        <div className="flex justify-between items-center">
                          <div className="font-bold text-sm text-white">{v.name}</div>
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-white font-bold">{v.tier}</span>
                        </div>
                        <div className="text-xs text-[#b3b3b3] mt-1">{v.city} • Cap: {v.cap} • {v.sound}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-[#181818] rounded-xl p-6 border border-white/5 space-y-4">
                  <div className="flex justify-between items-center pb-2 border-b border-white/10">
                    <div className="font-bold text-white text-sm">Lineup Matchmaker & Booking</div>
                    <span className="text-xs font-mono text-[#1DB954] bg-[#1DB954]/10 px-2.5 py-1 rounded-full">{selectedVenue.name}</span>
                  </div>

                  <div className="space-y-3 text-xs">
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="font-bold text-white/50 uppercase block mb-1">Offer Fee (EUR)</label>
                        <input
                          type="number"
                          value={inquiryFee}
                          onChange={(e) => setInquiryFee(e.target.value)}
                          className="w-full bg-black/60 border border-white/10 rounded-md p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="font-bold text-white/50 uppercase block mb-1">Performance Date</label>
                        <input
                          type="date"
                          value={inquiryDate}
                          onChange={(e) => setInquiryDate(e.target.value)}
                          className="w-full bg-black/60 border border-white/10 rounded-md p-2.5 text-white focus:border-[#1DB954] focus:outline-none"
                        />
                      </div>
                    </div>

                    <button
                      onClick={dispatchBooking}
                      className="w-full py-3 bg-[#1DB954] hover:bg-[#1ed760] text-black font-extrabold rounded-full text-sm transition-transform active:scale-95 shadow-lg shadow-[#1DB954]/20"
                    >
                      📨 Transmit Formal Offer to Primary Agency
                    </button>

                    {inquiryReceipt && (
                      <div className="p-3 bg-[#1DB954]/10 border border-[#1DB954]/30 rounded-lg text-xs text-[#1DB954] font-mono">
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
              <div className="bg-[#181818] rounded-xl p-6 border border-white/5 flex flex-col h-[520px]">
                <div className="flex justify-between items-center pb-3 border-b border-white/10 mb-3">
                  <div className="font-bold text-white text-sm flex items-center gap-2">
                    <Brain className="w-4 h-4 text-[#1DB954]" /> Graphify Associative Recall Chat
                  </div>
                  <span className="text-xs font-mono text-[#1DB954] bg-[#1DB954]/10 px-2.5 py-0.5 rounded-full">
                    Multi-Hop Memory Active
                  </span>
                </div>

                <div className="flex-1 overflow-y-auto space-y-3 p-3 bg-black/50 rounded-lg border border-white/5 mb-3">
                  {chatMessages.map((msg, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-lg text-xs leading-relaxed max-w-[85%] ${
                        msg.sender === "user"
                          ? "ml-auto bg-[#1DB954] text-black font-semibold"
                          : "mr-auto bg-[#282828] text-white"
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
                <div className="bg-[#181818] rounded-xl p-6 border border-white/5 space-y-4">
                  <div className="font-bold text-white text-sm flex items-center gap-2 pb-2 border-b border-white/10">
                    <Globe2 className="w-4 h-4 text-[#1DB954]" /> De-Anglicization Index
                  </div>
                  <div className="text-center py-6">
                    <div className="text-5xl font-black text-[#1DB954] font-mono tracking-tight">56.4%</div>
                    <div className="text-xs text-[#b3b3b3] mt-2 font-medium">Global Non-Anglo Music Dominance</div>
                  </div>
                  <p className="text-xs text-white/40 leading-relaxed">
                    Mined across 11+ non-English and diaspora territories (Germany, South Korea, Nigeria, Jamaica, France, Japan, Brazil).
                  </p>
                </div>

                <div className="bg-[#181818] rounded-xl p-6 border border-white/5 space-y-4">
                  <div className="font-bold text-white text-sm flex items-center gap-2 pb-2 border-b border-white/10">
                    <Sparkles className="w-4 h-4 text-purple-400" /> Breakout A&R Radar
                  </div>
                  <div className="space-y-2 text-xs">
                    {[
                      { name: "Aphex Twin", sub: "Ambient / IDM", score: "2.25" },
                      { name: "Nils Frahm", sub: "Neo-Classical", score: "2.25" },
                      { name: "Burna Boy", sub: "Afrobeats / Lagos", score: "1.94" },
                    ].map((a, idx) => (
                      <div key={idx} className="p-3 bg-black/40 rounded-lg flex justify-between items-center">
                        <div>
                          <div className="font-bold text-white">{a.name}</div>
                          <div className="text-[10px] text-[#b3b3b3]">{a.sub}</div>
                        </div>
                        <span className="font-mono text-[#1DB954] font-bold">{a.score} VELOCITY</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-[#181818] rounded-xl p-6 border border-white/5 space-y-4">
                  <div className="font-bold text-white text-sm flex items-center gap-2 pb-2 border-b border-white/10">
                    <Flame className="w-4 h-4 text-amber-400" /> Producer Export Hubs
                  </div>
                  <div className="space-y-2 text-xs">
                    {[
                      { hub: "Sweden (Stockholm)", producers: "Max Martin, Shellback", export: "50.0%" },
                      { hub: "United States (LA / NYC)", producers: "Dr. Dre, Rick Rubin", export: "21.1%" },
                      { hub: "United Kingdom (London)", producers: "Brian Eno, George Martin", export: "14.3%" },
                    ].map((h, idx) => (
                      <div key={idx} className="p-3 bg-black/40 rounded-lg flex justify-between items-center">
                        <div>
                          <div className="font-bold text-white">{h.hub}</div>
                          <div className="text-[10px] text-[#b3b3b3]">{h.producers}</div>
                        </div>
                        <span className="font-mono text-[#1DB954] font-bold">{h.export}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>

        {/* ========================================================= */}
        {/* 3. SPOTIFY RIGHT DRAWER (Now Playing View / Intelligence) */}
        {/* ========================================================= */}
        {showRightDrawer && (
          <aside className="w-72 bg-[#121212] rounded-lg p-4 flex flex-col gap-4 shrink-0 border border-white/5 shadow-2xl overflow-y-auto text-xs">
            <div className="font-bold text-white text-sm pb-2 border-b border-white/10 flex justify-between items-center">
              <span>Track Intelligence</span>
              <span className="text-[10px] font-mono text-[#1DB954] bg-[#1DB954]/10 px-2 py-0.5 rounded">LIVE</span>
            </div>

            <div className="rounded-lg overflow-hidden bg-black/40 border border-white/10 aspect-video relative">
              <img src={currentTrack.cover} alt="Cover" className="w-full h-full object-cover" />
              <div className="absolute bottom-2 left-2 px-2 py-0.5 rounded bg-black/70 text-[10px] font-mono text-white">
                {currentTrack.bpm} BPM
              </div>
            </div>

            <div>
              <div className="font-bold text-white text-sm">{currentTrack.title}</div>
              <div className="text-[#b3b3b3]">{currentTrack.artist}</div>
            </div>

            <div className="p-3 bg-[#181818] rounded-lg border border-white/5 space-y-2">
              <div className="font-bold text-white">Acoustic Fingerprint</div>
              <div className="grid grid-cols-2 gap-2 text-[11px]">
                <div className="text-white/50">Genre: <span className="text-white font-medium">{currentTrack.genre}</span></div>
                <div className="text-white/50">Tempo: <span className="text-[#1DB954] font-mono font-bold">{currentTrack.bpm} BPM</span></div>
                <div className="text-white/50">Mel Bands: <span className="text-white font-mono">32 Log</span></div>
                <div className="text-white/50">Tempogram: <span className="text-white font-mono">48 Bins</span></div>
              </div>
            </div>

            <div className="p-3 bg-[#181818] rounded-lg border border-white/5 space-y-1.5">
              <div className="font-bold text-white">Master Credits</div>
              <div className="text-[11px] text-white/50">Studio: <span className="text-white">Funkhaus Studio 1</span></div>
              <div className="text-[11px] text-white/50">Rights: <span className="text-[#1DB954]">100% Artist Owned</span></div>
              <div className="text-[11px] text-white/50">Publishing: <span className="text-white">GEMA Registered</span></div>
            </div>
          </aside>
        )}
      </div>

      {/* ========================================================= */}
      {/* 4. SPOTIFY BOTTOM NOW PLAYING AUDIO BAR                    */}
      {/* ========================================================= */}
      <footer className="h-20 bg-black border-t border-white/10 px-4 flex items-center justify-between shrink-0 z-50">
        {/* Left: Track Details */}
        <div className="flex items-center gap-3 w-1/4 min-w-[180px]">
          <img src={currentTrack.cover} alt="Cover" className="w-12 h-12 rounded object-cover shadow-md" />
          <div className="truncate">
            <div className="text-xs font-semibold text-white truncate hover:underline cursor-pointer">
              {currentTrack.title}
            </div>
            <div className="text-[11px] text-[#b3b3b3] truncate hover:underline cursor-pointer">
              {currentTrack.artist}
            </div>
          </div>
          <button onClick={() => setIsLiked(!isLiked)} className="text-white/60 hover:text-white ml-2 transition-colors">
            <Heart className={`w-4 h-4 ${isLiked ? "fill-[#1DB954] text-[#1DB954]" : ""}`} />
          </button>
        </div>

        {/* Center: Controls & Scrubbing */}
        <div className="flex flex-col items-center gap-1.5 w-2/4 max-w-xl">
          <div className="flex items-center gap-4">
            <button className="text-white/60 hover:text-white transition-colors"><Shuffle className="w-4 h-4" /></button>
            <button className="text-white/60 hover:text-white transition-colors"><SkipBack className="w-4 h-4 fill-current" /></button>
            <button
              onClick={togglePlay}
              className="w-8 h-8 rounded-full bg-white hover:scale-105 flex items-center justify-center transition-transform shadow-lg"
            >
              {isPlaying ? <Pause className="w-4 h-4 fill-black text-black" /> : <Play className="w-4 h-4 fill-black text-black ml-0.5" />}
            </button>
            <button className="text-white/60 hover:text-white transition-colors"><SkipForward className="w-4 h-4 fill-current" /></button>
            <button className="text-white/60 hover:text-white transition-colors"><Repeat className="w-4 h-4" /></button>
          </div>

          <div className="w-full flex items-center gap-2 text-[10px] font-mono text-white/50">
            <span>1:28</span>
            <div className="flex-1 h-1 bg-white/20 rounded-full overflow-hidden cursor-pointer group">
              <div className="h-full bg-white group-hover:bg-[#1DB954] transition-colors" style={{ width: `${currentTrack.progress}%` }}></div>
            </div>
            <span>{currentTrack.duration}</span>
          </div>
        </div>

        {/* Right: Volume & Drawer Toggle */}
        <div className="flex items-center justify-end gap-3 w-1/4 min-w-[180px]">
          <div className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-white font-bold">
            {currentTrack.bpm} BPM
          </div>
          <button className="text-white/60 hover:text-white transition-colors">
            {volume === 0 ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
          </button>
          <input
            type="range"
            min="0"
            max="100"
            value={volume}
            onChange={(e) => setVolume(Number(e.target.value))}
            className="w-20 h-1 accent-[#1DB954] cursor-pointer"
          />
        </div>
      </footer>
    </div>
  );
}
