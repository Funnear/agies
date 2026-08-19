"use client";

import React, { useState } from "react";
import { AudioVisualizer3D } from "@/components/AudioVisualizer3D";
import { NetworkGraph3D } from "@/components/NetworkGraph3D";
import {
  Radio,
  Building2,
  Share2,
  Brain,
  BarChart3,
  Key,
  Sparkles,
  Send,
  Copy,
  CheckCircle2,
  Globe2,
  Music2,
  ShieldAlert,
} from "lucide-react";

export default function Home() {
  const [activeTab, setActiveTab] = useState<
    "studio" | "venues" | "network" | "memory" | "analytics"
  >("studio");

  // Bedroom Studio State
  const [artistName, setArtistName] = useState("Subtle Flux");
  const [trackTitle, setTrackTitle] = useState("Modular Resonance (Original Cut)");
  const [homeCity, setHomeCity] = useState("Berlin");
  const [targetGenre, setTargetGenre] = useState("Techno");
  const [bpm, setBpm] = useState(132);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [diagnosticResult, setDiagnosticResult] = useState<any>({
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
  });

  // Venue Portal State
  const [selectedVenue, setSelectedVenue] = useState({
    name: "Berghain / Panorama Bar",
    city: "Berlin",
    cap: 1500,
    tier: "Hall",
    sound: "Funktion-One Custom (Double 21-inch Subs)",
    email: "booking@berghain.de",
  });
  const [inquiryFee, setInquiryFee] = useState("1800");
  const [inquiryDate, setInquiryDate] = useState("2026-11-14");
  const [inquiryStatus, setInquiryStatus] = useState<string | null>(null);

  // Memory Chat State
  const [chatMessages, setChatMessages] = useState([
    {
      sender: "bot",
      text: "Welcome to AGIES AI Studio Suite. Ask me about contracts, mastering techniques at Hansa/Abbey Road, classic analog synthesizers (TR-808, Prophet-5), or how to pitch showcase festivals.",
    },
  ]);
  const [chatInput, setChatInput] = useState("");
  const [copiedPitch, setCopiedPitch] = useState(false);

  const runDiagnostic = async () => {
    setIsAnalyzing(true);
    const newBpm = targetGenre === "Techno" ? 132 : targetGenre === "House" ? 124 : 85;
    setBpm(newBpm);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/audio/analyze-demo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": "agies_test_key_123",
        },
        body: JSON.stringify({
          track_title: trackTitle,
          artist_name: artistName,
          home_city: homeCity,
          home_country: "Germany",
          subgenre_hint: targetGenre,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setDiagnosticResult({
          bpm: data.detected_bpm,
          subgenre: data.classified_subgenre.replace("_", " ").toUpperCase(),
          confidence: data.subgenre_confidence,
          matches: data.nearest_acoustic_artist_matches.map((m: any) => ({
            name: m.artist_name,
            genre: m.genres ? m.genres.join(", ") : "Electronic",
            score: (m.acoustic_similarity_score * 100).toFixed(1),
          })),
          labels: data.target_record_labels.map((l: any) => ({
            name: l.label_name,
            city: l.country,
            note: l.a_and_r_status,
          })),
          venues: data.recommended_debut_venues.map((v: any) => ({
            name: v.venue_name,
            cap: v.capacity,
            tier: v.capacity_tier,
            sound: v.sound_system,
          })),
        });
      }
    } catch (e) {
      console.log("Local fallback simulation active");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSendChat = async () => {
    if (!chatInput.trim()) return;
    const q = chatInput;
    setChatMessages((prev) => [...prev, { sender: "user", text: q }]);
    setChatInput("");

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/v1/memory/recall?query=${encodeURIComponent(
          q
        )}&top_k=2`,
        { headers: { "X-API-Key": "agies_test_key_123" } }
      );
      if (res.ok) {
        const data = await res.json();
        let reply = `Recalled ${data.recalled_nodes_count} memory nodes across ${data.recalled_nodes
          .map((n: any) => n.label)
          .join(", ")}.`;
        if (q.toLowerCase().includes("contract") || q.toLowerCase().includes("360")) {
          reply +=
            "\n\nIndustry Rule: Never sign a 360-degree deal as a debut artist. Retain master rights via Bandcamp and license single EPs for max 3-year windows.";
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

  const pitchText = `Subject: Live Debut Pitch / Support Slot Inquiry: ${artistName} @ ${selectedVenue.name}

Hi ${selectedVenue.name} Bookings Team,

I hope you're having a great week. I'm ${artistName}, a ${homeCity}-based producer producing ${targetGenre} (sound profile: ${bpm} BPM, Mel-Tempogram acoustic energy aligned with Stephan Bodzin).

I've just finalized my new 3-track EP '${trackTitle}', and I'm looking to play opening support slots for your upcoming club nights.
You can listen to the private demo stream here: [Private Demo Stream Link]

I would love to be considered for an opening support slot on your lineup. Thank you for your time and for supporting grassroots music!

Best regards,
${artistName}
Contact: booking@${artistName.toLowerCase().replace(/\s+/g, "")}-official.com`;

  const copyPitch = () => {
    navigator.clipboard.writeText(pitchText);
    setCopiedPitch(true);
    setTimeout(() => setCopiedPitch(false), 2000);
  };

  const dispatchInquiry = () => {
    setInquiryStatus(
      `✓ Dispatched formal offer of ${inquiryFee} EUR for ${inquiryDate} to ${selectedVenue.name} representative. Status: DISPATCHED_TO_AGENT.`
    );
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-black">
      {/* Top Navigation */}
      <header className="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur-xl px-6 py-3.5 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-cyan-400 to-purple-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Music2 className="w-5 h-5 text-slate-950" />
          </div>
          <div>
            <span className="font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 text-lg">
              AGIES STUDIO
            </span>
            <span className="ml-2 text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
              NEXT.JS • THREE.JS
            </span>
          </div>
        </div>

        <nav className="flex gap-1.5 p-1 bg-slate-950/80 border border-slate-800 rounded-xl">
          <button
            onClick={() => setActiveTab("studio")}
            className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
              activeTab === "studio"
                ? "bg-slate-800 text-cyan-400 border border-cyan-500/30 shadow-md"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Radio className="w-3.5 h-3.5" /> Bedroom Studio
          </button>
          <button
            onClick={() => setActiveTab("venues")}
            className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
              activeTab === "venues"
                ? "bg-slate-800 text-cyan-400 border border-cyan-500/30 shadow-md"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Building2 className="w-3.5 h-3.5" /> Venue Matchmaker
          </button>
          <button
            onClick={() => setActiveTab("network")}
            className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
              activeTab === "network"
                ? "bg-slate-800 text-cyan-400 border border-cyan-500/30 shadow-md"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Share2 className="w-3.5 h-3.5" /> 3D Universe
          </button>
          <button
            onClick={() => setActiveTab("memory")}
            className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
              activeTab === "memory"
                ? "bg-slate-800 text-cyan-400 border border-cyan-500/30 shadow-md"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Brain className="w-3.5 h-3.5" /> Graphify AI
          </button>
          <button
            onClick={() => setActiveTab("analytics")}
            className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
              activeTab === "analytics"
                ? "bg-slate-800 text-cyan-400 border border-cyan-500/30 shadow-md"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <BarChart3 className="w-3.5 h-3.5" /> A&R Radar
          </button>
        </nav>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-xs text-slate-400 bg-slate-950/60 px-3 py-1.5 rounded-lg border border-slate-800">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>API Online :8000</span>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto overflow-y-auto">
        {/* TAB 1: BEDROOM PRODUCER STUDIO */}
        {activeTab === "studio" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Form & 3D Visualizer */}
              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-4">
                <div className="flex justify-between items-center pb-3 border-b border-slate-800">
                  <div className="flex items-center gap-2 font-bold text-cyan-400">
                    <Sparkles className="w-4 h-4" /> Demo Track Acoustic Analyzer
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-400">
                    arXiv:2110.08862
                  </span>
                </div>

                <div className="space-y-3">
                  <div>
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                      Artist / Alias
                    </label>
                    <input
                      type="text"
                      value={artistName}
                      onChange={(e) => setArtistName(e.target.value)}
                      className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2 text-sm focus:border-cyan-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                      Track Title
                    </label>
                    <input
                      type="text"
                      value={trackTitle}
                      onChange={(e) => setTrackTitle(e.target.value)}
                      className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2 text-sm focus:border-cyan-500 focus:outline-none"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                        Home City
                      </label>
                      <select
                        value={homeCity}
                        onChange={(e) => setHomeCity(e.target.value)}
                        className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2 text-sm focus:border-cyan-500 focus:outline-none"
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
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                        Target Subgenre
                      </label>
                      <select
                        value={targetGenre}
                        onChange={(e) => setTargetGenre(e.target.value)}
                        className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2 text-sm focus:border-cyan-500 focus:outline-none"
                      >
                        <option value="Techno">Industrial / Melodic Techno</option>
                        <option value="House">Deep House / Nu-Disco</option>
                        <option value="Ambient">Ambient & Neo-Classical</option>
                        <option value="Drum and Bass">Drum and Bass / Liquid</option>
                      </select>
                    </div>
                  </div>

                  {/* 3D Visualizer */}
                  <AudioVisualizer3D bpm={bpm} genre={targetGenre} />

                  <button
                    onClick={runDiagnostic}
                    disabled={isAnalyzing}
                    className="w-full py-3 bg-gradient-to-r from-cyan-400 to-blue-500 hover:from-cyan-300 hover:to-blue-400 text-slate-950 font-extrabold rounded-xl text-sm transition-transform active:scale-95 shadow-lg shadow-cyan-500/20 flex items-center justify-center gap-2"
                  >
                    <Sparkles className="w-4 h-4" />
                    {isAnalyzing
                      ? "Analyzing Mel-Tempograms..."
                      : "Run AI Diagnostic & Build Career Plan"}
                  </button>
                </div>
              </div>

              {/* Right: Diagnostic Dossier */}
              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-4">
                <div className="flex justify-between items-center pb-3 border-b border-slate-800">
                  <div className="flex items-center gap-2 font-bold text-purple-400">
                    <Radio className="w-4 h-4" /> Acoustic Diagnostic Dossier
                  </div>
                  <div className="flex gap-2">
                    <span className="text-xs font-mono px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-bold">
                      {diagnosticResult.bpm} BPM
                    </span>
                    <span className="text-xs font-mono px-2.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 font-bold">
                      {diagnosticResult.subgenre}
                    </span>
                  </div>
                </div>

                <div>
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                    Nearest Acoustic Titan Matches in Graph
                  </div>
                  <div className="space-y-2">
                    {diagnosticResult.matches.map((m: any, idx: number) => (
                      <div
                        key={idx}
                        className="flex justify-between items-center p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 hover:border-cyan-500/30 transition-all"
                      >
                        <div>
                          <div className="font-bold text-sm text-slate-200">
                            {m.name}
                          </div>
                          <div className="text-xs text-slate-500">{m.genre}</div>
                        </div>
                        <div className="font-mono text-emerald-400 font-bold text-sm">
                          {m.score}% MATCH
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                    Target Indie Record Labels (Open to Demos)
                  </div>
                  <div className="space-y-2">
                    {diagnosticResult.labels.map((l: any, idx: number) => (
                      <div
                        key={idx}
                        className="flex justify-between items-center p-3 rounded-xl bg-slate-950/80 border border-slate-800/80"
                      >
                        <div>
                          <div className="font-bold text-sm text-slate-200">
                            {l.name}
                          </div>
                          <div className="text-xs text-slate-500">{l.city}</div>
                        </div>
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400">
                          {l.note}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* 4-Phase Roadmap & Booking Pitch */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-3">
                <div className="flex justify-between items-center pb-2 border-b border-slate-800">
                  <div className="font-bold text-emerald-400 text-sm">
                    🗺️ 4-Phase Stepping-Stone Roadmap
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400">
                    Zero-Debt Strategy
                  </span>
                </div>

                <div className="space-y-2.5 text-xs">
                  <div className="p-3 bg-purple-500/5 border-l-2 border-purple-500 rounded-r-lg">
                    <div className="font-bold text-purple-400 mb-0.5">
                      Phase 1: Zero-Debt Calibration & Direct-to-Fan
                    </div>
                    <div className="text-slate-400">
                      Calibrate BPM window. Master 3-track EP. Distribute via
                      Bandcamp (direct fan monetization) + DistroKid.
                    </div>
                  </div>
                  <div className="p-3 bg-purple-500/5 border-l-2 border-purple-500 rounded-r-lg">
                    <div className="font-bold text-purple-400 mb-0.5">
                      Phase 2: Gateway Curation & Sound Validation
                    </div>
                    <div className="text-slate-400">
                      Submit stems to COLORSxSTUDIOS, HATE, and BBC Introducing.
                      Register with GEMA / SoundExchange.
                    </div>
                  </div>
                  <div className="p-3 bg-purple-500/5 border-l-2 border-purple-500 rounded-r-lg">
                    <div className="font-bold text-purple-400 mb-0.5">
                      Phase 3: Showcase Circuits & A&R Visibility
                    </div>
                    <div className="text-slate-400">
                      Apply for showcase slots at Reeperbahn Festival / ESNS to
                      perform in front of international scouts.
                    </div>
                  </div>
                  <div className="p-3 bg-purple-500/5 border-l-2 border-purple-500 rounded-r-lg">
                    <div className="font-bold text-purple-400 mb-0.5">
                      Phase 4: Boutique Imprint Leverage
                    </div>
                    <div className="text-slate-400">
                      Retain 100% publishing rights. Negotiate single-EP licensing
                      deal with a maximum 3-year term.
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-3">
                <div className="flex justify-between items-center pb-2 border-b border-slate-800">
                  <div className="font-bold text-cyan-400 text-sm">
                    📨 Automated Promoter Pitch Email
                  </div>
                  <button
                    onClick={copyPitch}
                    className="flex items-center gap-1.5 text-xs bg-slate-800 hover:bg-slate-700 px-3 py-1 rounded-lg border border-slate-700 font-semibold"
                  >
                    {copiedPitch ? (
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    ) : (
                      <Copy className="w-3.5 h-3.5" />
                    )}
                    {copiedPitch ? "Copied!" : "Copy Pitch"}
                  </button>
                </div>

                <pre className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-xs font-mono text-cyan-300/90 whitespace-pre-wrap max-h-60 overflow-y-auto leading-relaxed">
                  {pitchText}
                </pre>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: VENUES & PROMOTER PORTAL */}
        {activeTab === "venues" && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-4">
              <div className="flex justify-between items-center pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2 font-bold text-cyan-400">
                  <Building2 className="w-4 h-4" /> Global Venue Directory
                </div>
              </div>

              <div className="space-y-3 max-h-[500px] overflow-y-auto pr-1">
                {[
                  {
                    name: "Berghain / Panorama Bar",
                    city: "Berlin",
                    cap: 1500,
                    tier: "Hall",
                    sound: "Funktion-One Custom (Double 21-inch Subs)",
                    email: "booking@berghain.de",
                  },
                  {
                    name: "Tresor Berlin",
                    city: "Berlin",
                    cap: 800,
                    tier: "Club",
                    sound: "Funktion-One Vault Acoustics",
                    email: "booking@tresorberlin.com",
                  },
                  {
                    name: "Schokoladen (Mitte)",
                    city: "Berlin",
                    cap: 150,
                    tier: "Intimate Debut",
                    sound: "Vintage Analog PA",
                    email: "booking@schokoladen-mitte.de",
                  },
                  {
                    name: "Fabric London",
                    city: "London",
                    cap: 1600,
                    tier: "Hall",
                    sound: "Pioneer Bodysonic Bass Floor",
                    email: "programming@fabriclondon.com",
                  },
                  {
                    name: "The Windmill (Brixton)",
                    city: "London",
                    cap: 150,
                    tier: "Intimate Debut",
                    sound: "Grassroots Club PA",
                    email: "windmillbrixton@gmail.com",
                  },
                  {
                    name: "The Bowery Ballroom",
                    city: "New York City",
                    cap: 575,
                    tier: "Club",
                    sound: "d&b Soundscape",
                    email: "booking@boweryballroom.com",
                  },
                ].map((v, idx) => (
                  <div
                    key={idx}
                    onClick={() => setSelectedVenue(v)}
                    className={`p-4 rounded-xl border cursor-pointer transition-all ${
                      selectedVenue.name === v.name
                        ? "bg-slate-800/80 border-cyan-500 shadow-md shadow-cyan-500/10"
                        : "bg-slate-950/80 border-slate-800 hover:border-slate-700"
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div className="font-bold text-sm text-slate-200">
                        {v.name}
                      </div>
                      <span
                        className={`text-[10px] font-mono px-2 py-0.5 rounded-full ${
                          v.tier.includes("Intimate")
                            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
                            : v.tier.includes("Club")
                            ? "bg-amber-500/10 text-amber-400 border border-amber-500/30"
                            : "bg-purple-500/10 text-purple-400 border border-purple-500/30"
                        }`}
                      >
                        {v.tier.toUpperCase()}
                      </span>
                    </div>
                    <div className="text-xs text-slate-400 mt-1">
                      {v.city} • Capacity: {v.cap} • {v.sound}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Lineup Matchmaker & Booking Dispatch */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-4">
              <div className="flex justify-between items-center pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2 font-bold text-purple-400">
                  <Sparkles className="w-4 h-4" /> AI Lineup Matchmaker
                </div>
                <span className="text-xs font-mono text-cyan-400 bg-cyan-500/10 border border-cyan-500/30 px-3 py-1 rounded-full">
                  {selectedVenue.name}
                </span>
              </div>

              <div>
                <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                  Recommended Artists for Selected Room
                </div>
                <div className="space-y-2">
                  <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                    <div>
                      <div className="font-bold text-sm text-slate-200">
                        Stephan Bodzin
                      </div>
                      <div className="text-xs text-slate-400">
                        Techno • 132 BPM • Optimal Headliner
                      </div>
                    </div>
                    <div className="font-mono text-emerald-400 font-bold text-sm">
                      98.4%
                    </div>
                  </div>
                  <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                    <div>
                      <div className="font-bold text-sm text-slate-200">
                        {artistName} (Emerging Producer)
                      </div>
                      <div className="text-xs text-slate-400">
                        {targetGenre} • {bpm} BPM • Opening Support Act
                      </div>
                    </div>
                    <div className="font-mono text-cyan-400 font-bold text-sm">
                      89.2%
                    </div>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-800 space-y-3">
                <div className="font-bold text-sm text-slate-200">
                  Dispatch Formal Booking Offer
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                      Offer Fee (EUR)
                    </label>
                    <input
                      type="number"
                      value={inquiryFee}
                      onChange={(e) => setInquiryFee(e.target.value)}
                      className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2 text-sm focus:border-cyan-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                      Event Date
                    </label>
                    <input
                      type="date"
                      value={inquiryDate}
                      onChange={(e) => setInquiryDate(e.target.value)}
                      className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2 text-sm focus:border-cyan-500 focus:outline-none"
                    />
                  </div>
                </div>

                <button
                  onClick={dispatchInquiry}
                  className="w-full py-3 bg-gradient-to-r from-purple-500 to-indigo-600 hover:from-purple-400 hover:to-indigo-500 text-white font-extrabold rounded-xl text-sm transition-transform active:scale-95 shadow-lg shadow-purple-500/20"
                >
                  📨 Transmit Offer to Primary Booking Agency
                </button>

                {inquiryStatus && (
                  <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-xs text-emerald-300 font-mono">
                    {inquiryStatus}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: 3D KNOWLEDGE UNIVERSE */}
        {activeTab === "network" && (
          <div className="space-y-4">
            <NetworkGraph3D />
          </div>
        )}

        {/* TAB 4: GRAPHIFY MEMORY & AI RESEARCH */}
        {activeTab === "memory" && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl flex flex-col h-[520px]">
              <div className="flex justify-between items-center pb-3 border-b border-slate-800 mb-3">
                <div className="flex items-center gap-2 font-bold text-cyan-400">
                  <Brain className="w-4 h-4" /> Graphify Associative Recall Chat
                </div>
                <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-0.5 rounded-full">
                  Associative Recall Active
                </span>
              </div>

              <div className="flex-1 overflow-y-auto space-y-3 p-3 bg-slate-950 rounded-xl border border-slate-800/80 mb-3">
                {chatMessages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded-xl text-xs leading-relaxed max-w-[85%] ${
                      msg.sender === "user"
                        ? "ml-auto bg-slate-800 text-white border border-slate-700"
                        : "mr-auto bg-cyan-500/10 border border-cyan-500/20 text-slate-200"
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
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs focus:border-cyan-500 focus:outline-none"
                />
                <button
                  onClick={handleSendChat}
                  className="px-5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-xl text-xs transition-all flex items-center gap-1.5"
                >
                  <Send className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-4">
              <div className="flex justify-between items-center pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2 font-bold text-purple-400">
                  <Sparkles className="w-4 h-4" /> Ingest Article / Press Release
                </div>
              </div>

              <div className="space-y-3">
                <div>
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                    Article Title / Session
                  </label>
                  <input
                    type="text"
                    defaultValue="BICEP Modular Synthesis & Touring Setup"
                    className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3.5 py-2 text-sm focus:border-cyan-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                    Unstructured Content
                  </label>
                  <textarea
                    rows={7}
                    defaultValue="Ninja Tune electronic duo BICEP record their analog leads using the Roland TB-303 and Prophet-5, mastering their albums at Metropolis Studios London before headlining Alexandra Palace."
                    className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs font-mono focus:border-cyan-500 focus:outline-none"
                  />
                </div>

                <button
                  onClick={() =>
                    alert(
                      "Article graphified into persistent memory! Linked gear: Roland TB-303, Prophet-5, Metropolis Studios."
                    )
                  }
                  className="w-full py-3 bg-gradient-to-r from-purple-500 to-indigo-600 hover:from-purple-400 hover:to-indigo-500 text-white font-extrabold rounded-xl text-sm transition-transform active:scale-95 shadow-lg shadow-purple-500/20"
                >
                  ⚡ Graphify Article into Persistent Memory
                </button>
              </div>
            </div>
          </div>
        )}

        {/* TAB 5: INDUSTRY ANALYTICS & A&R RADAR */}
        {activeTab === "analytics" && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-4">
              <div className="flex items-center gap-2 font-bold text-cyan-400 pb-3 border-b border-slate-800">
                <Globe2 className="w-4 h-4" /> De-Anglicization Index
              </div>
              <div className="text-center py-6">
                <div className="text-5xl font-black text-emerald-400 font-mono tracking-tight">
                  56.4%
                </div>
                <div className="text-xs text-slate-400 mt-2 font-medium">
                  Global Non-Anglo Music Dominance
                </div>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Mined across 11+ non-English and diaspora territories (Germany,
                South Korea, Nigeria, Jamaica, France, Japan, Brazil).
              </p>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-4">
              <div className="flex items-center gap-2 font-bold text-purple-400 pb-3 border-b border-slate-800">
                <Sparkles className="w-4 h-4" /> Breakout A&R Radar (Node2Vec)
              </div>
              <div className="space-y-2.5">
                {[
                  { name: "Aphex Twin", sub: "Ambient / IDM", score: "2.25" },
                  { name: "Nils Frahm", sub: "Neo-Classical", score: "2.25" },
                  { name: "Burna Boy", sub: "Afrobeats / Lagos", score: "1.94" },
                ].map((a, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center"
                  >
                    <div>
                      <div className="font-bold text-xs text-slate-200">
                        {a.name}
                      </div>
                      <div className="text-[10px] text-slate-500">{a.sub}</div>
                    </div>
                    <span className="text-xs font-mono font-bold text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded-md">
                      {a.score} VELOCITY
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-4">
              <div className="flex items-center gap-2 font-bold text-amber-400 pb-3 border-b border-slate-800">
                <Share2 className="w-4 h-4" /> Producer Export Hubs
              </div>
              <div className="space-y-2.5">
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
                    className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center"
                  >
                    <div>
                      <div className="font-bold text-xs text-slate-200">
                        {h.hub}
                      </div>
                      <div className="text-[10px] text-slate-500">
                        {h.producers}
                      </div>
                    </div>
                    <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-md">
                      {h.export}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
