"use client";

import React, { useEffect, useRef, useState, useCallback } from "react";
import * as d3 from "d3";
import {
  Globe2,
  Sparkles,
  Maximize2,
  Minimize2,
  Play,
  Pause,
  RotateCw,
  Zap,
  Activity,
  PlusCircle,
  ZoomIn,
  ZoomOut,
  Layers,
  Compass,
} from "lucide-react";
import { useAppDispatch } from "@/store";
import { setTrack, setIsPlaying } from "@/store/playerSlice";

export interface D3Node extends d3.SimulationNodeDatum {
  id: string;
  name: string;
  category: "city" | "artist" | "venue" | "studio" | "label" | "festival" | "gear" | "genre";
  country?: string;
  color: string;
  radius: number;
  description: string;
  connections: string[];
  soundSystem?: string;
  bpm?: number;
  genre?: string;
  isNew?: boolean;
}

export interface D3Link extends d3.SimulationLinkDatum<D3Node> {
  source: string | D3Node;
  target: string | D3Node;
  relType?: string;
}

// Initial Base Seed Nodes
const INITIAL_D3_NODES: D3Node[] = [
  // === GLOBAL CITIES (Cyan #00f0ff) ===
  { id: "city_berlin", name: "Berlin Hub", category: "city", country: "Germany", color: "#00f0ff", radius: 22, description: "Temple of global techno, modular synthesis, and acoustic recording sanctuaries.", connections: ["city_london", "city_saopaulo", "std_hansa", "ven_berghain", "lbl_ostgut"] },
  { id: "city_london", name: "London Hub", category: "city", country: "United Kingdom", color: "#00f0ff", radius: 22, description: "International music industry capital, breakbeat lineage, and major label hub.", connections: ["city_berlin", "city_la", "city_mumbai", "std_abbeyroad", "ven_fabric", "lbl_warp"] },
  { id: "city_mumbai", name: "Mumbai Hub", category: "city", country: "India", color: "#00f0ff", radius: 22, description: "National commercial, hip-hop, and electronic capital (antiSOCIAL, YRF Studios, Azadi Records).", connections: ["city_london", "city_goa", "ven_antisocial_mumbai", "std_yrf_mumbai", "art_divine"] },
  { id: "city_goa", name: "Goa Coastal Hub", category: "city", country: "India", color: "#00f0ff", radius: 20, description: "Global spiritual capital of Goa Trance & coastal sunset deep house (HillTop, Shiva Valley, Anjuna).", connections: ["city_mumbai", "city_berlin", "ven_hilltop_goa", "cur_anjuna_goa"] },
  { id: "city_la", name: "Los Angeles Hub", category: "city", country: "United States", color: "#00f0ff", radius: 22, description: "Streaming giant epicenter, film scoring capital, and commercial pop hitmaking.", connections: ["city_london", "city_tokyo", "std_sunsetsound"] },
  { id: "city_tokyo", name: "Tokyo Hub", category: "city", country: "Japan", color: "#00f0ff", radius: 20, description: "Audiophile jazz kissaten culture, Shibuya-kei, and experimental electronic sound.", connections: ["city_la", "city_london", "ven_womb"] },
  { id: "city_saopaulo", name: "São Paulo Hub", category: "city", country: "Brazil", color: "#00f0ff", radius: 20, description: "Latin America's underground techno fortress, Barra Funda warehouses, and D-Edge sound.", connections: ["city_berlin", "ven_warung"] },
  { id: "city_barcelona", name: "Barcelona Hub", category: "city", country: "Spain", color: "#00f0ff", radius: 20, description: "Mediterranean electronic epicenter, Sónar Festival hub, and Poblenou warehouse scene.", connections: ["city_berlin", "fest_sonar"] },

  // === VENUES (Gold #eab308) ===
  { id: "ven_berghain", name: "Berghain / Panorama Bar", category: "venue", color: "#eab308", radius: 16, soundSystem: "Funktion-One Custom 4-Way Array", description: "Former GDR heating plant turned world capital of hedonistic industrial techno.", connections: ["city_berlin", "lbl_ostgut"] },
  { id: "ven_antisocial_mumbai", name: "antiSOCIAL Mumbai", category: "venue", color: "#eab308", radius: 15, soundSystem: "Subterranean Todi Mills Club PA", description: "Underground warehouse bunker for cutting-edge techno, modular live sets, and hip-hop cyphers.", connections: ["city_mumbai", "art_divine"] },
  { id: "ven_hilltop_goa", name: "HillTop Goa (Vagator)", category: "venue", color: "#eab308", radius: 16, soundSystem: "Full-Spectrum Open-Air Psychoacoustic Array", description: "The global spiritual mecca of Goa trance perched on Vagator's hills since the early 1980s.", connections: ["city_goa", "cur_anjuna_goa"] },
  { id: "ven_warung", name: "Warung Beach Club", category: "venue", color: "#eab308", radius: 15, soundSystem: "Funktion-One Wooden Temple Rig", description: "Open-air temple in Praia Brava surrounded by the Atlantic rainforest.", connections: ["city_saopaulo"] },
  { id: "ven_fabric", name: "Fabric London", category: "venue", color: "#eab308", radius: 15, soundSystem: "Bodysonic Vibrating Dancefloor", description: "Pioneering Farringdon subterranean club with bass transducers in the dancefloor.", connections: ["city_london"] },

  // === STUDIOS (Sky Blue #38bdf8) ===
  { id: "std_hansa", name: "Hansa Studios Berlin", category: "studio", color: "#38bdf8", radius: 14, description: "Legendary Meistersaal studio where David Bowie and Depeche Mode recorded.", connections: ["city_berlin"] },
  { id: "std_abbeyroad", name: "Abbey Road Studios", category: "studio", color: "#38bdf8", radius: 14, description: "World's most famous acoustic recording studio (The Beatles, Pink Floyd).", connections: ["city_london"] },
  { id: "std_sunsetsound", name: "Sunset Sound LA", category: "studio", color: "#38bdf8", radius: 14, description: "Iconic Hollywood studio home to custom discrete consoles and live acoustic chambers.", connections: ["city_la"] },

  // === ARTISTS (Purple #c084fc) ===
  { id: "art_divine", name: "DIVINE (Gully Gang)", category: "artist", color: "#c084fc", radius: 15, bpm: 135, genre: "Gully Rap", description: "Pioneer of Mumbai's street hip-hop revolution signed to Mass Appeal India.", connections: ["city_mumbai", "ven_antisocial_mumbai"] },
  { id: "art_stephanbodzin", name: "Stephan Bodzin", category: "artist", color: "#c084fc", radius: 14, bpm: 126, genre: "Melodic Techno", description: "Hardware live master sculpting hypnotic Moog Sub 37 synthesizer melodies.", connections: ["city_berlin", "ven_berghain"] },
  { id: "art_nilsfrahm", name: "Nils Frahm", category: "artist", color: "#c084fc", radius: 14, bpm: 110, genre: "Neo-Classical", description: "Acoustic innovator merging custom upright pianos with Roland Space Echoes in Saal 3.", connections: ["city_berlin"] },

  // === CURATORS & FESTIVALS (Rose #fb7185) ===
  { id: "cur_anjuna_goa", name: "Anjunadeep Open Air Goa", category: "festival", color: "#fb7185", radius: 16, bpm: 123, genre: "Melodic House", description: "Anjuna beachfront showcase blending analog Prophet-6 pad swells with sunset melodic deep house.", connections: ["city_goa", "ven_hilltop_goa"] },
  { id: "fest_sonar", name: "Sónar+D Barcelona", category: "festival", color: "#fb7185", radius: 15, description: "Pioneering Barcelona congress for advanced electronic music and AI creative tech.", connections: ["city_barcelona"] },
  { id: "lbl_ostgut", name: "Ostgut Ton", category: "label", color: "#f43f5e", radius: 13, description: "In-house label imprint of Berghain documenting pure underground club culture.", connections: ["city_berlin", "ven_berghain"] },
  { id: "lbl_warp", name: "Warp Records", category: "label", color: "#f43f5e", radius: 13, description: "Sheffield/London avant-garde label home to Aphex Twin, Boards of Canada, and Flying Lotus.", connections: ["city_london"] },
];

// Dynamic Stream Ingestion Pool
const DYNAMIC_INGESTION_POOL: Omit<D3Node, "x" | "y" | "vx" | "vy">[] = [
  { id: "ven_rso_berlin", name: "RSO.BERLIN (Schöneweide)", category: "venue", color: "#eab308", radius: 14, description: "Raw industrial warehouse bunker and home to Herrensauna marathon sessions.", connections: ["city_berlin", "coll_herrensauna"] },
  { id: "coll_herrensauna", name: "Herrensauna Collective", category: "artist", color: "#c084fc", radius: 15, bpm: 148, genre: "Industrial Techno", description: "148+ BPM relentless fast techno brotherhood founded by CEM and MCMLXXXV.", connections: ["ven_rso_berlin", "city_berlin"] },
  { id: "std_yrf_mumbai", name: "YRF Studios (Andheri West)", category: "studio", color: "#38bdf8", radius: 14, description: "Dolby Atmos Premier scoring stages and SSL Duality mixing consoles.", connections: ["city_mumbai"] },
  { id: "lbl_azadi", name: "Azadi Records", category: "label", color: "#f43f5e", radius: 14, description: "Pioneering South Asian socio-political hip-hop label (Seedhe Maut, Prabh Deep).", connections: ["city_mumbai", "city_delhi"] },
  { id: "city_delhi", name: "New Delhi Hub", category: "city", country: "India", color: "#00f0ff", radius: 20, description: "Northern hip-hop, live jazz cabaret, and Magnetic Fields festival axis.", connections: ["city_mumbai", "lbl_azadi"] },
  { id: "subg_amapiano", name: "Amapiano (Soweto Log-Drum)", category: "genre", color: "#a855f7", radius: 15, bpm: 114, genre: "House", description: "South African viral movement driven by FM log-drum sub-basslines and airy jazz keys.", connections: ["city_joburg"] },
  { id: "city_joburg", name: "Johannesburg Hub", category: "city", country: "South Africa", color: "#00f0ff", radius: 20, description: "Amapiano capital, Soweto sound system heritage, and Mzansi deep house.", connections: ["subg_amapiano", "city_london"] },
  { id: "ven_conne_island", name: "Conne Island Leipzig", category: "venue", color: "#eab308", radius: 13, description: "Historic Connewitz underground bastion for dubstep, punk, and bass culture.", connections: ["city_berlin"] },
  { id: "cur_boiler_room_mumbai", name: "Boiler Room Mumbai", category: "festival", color: "#fb7185", radius: 15, bpm: 135, genre: "Gully Bass", description: "Global underground livestream documenting authentic Mumbai street cyphers.", connections: ["city_mumbai", "art_divine"] },
  { id: "cur_cercle_colosseum", name: "Cercle Colosseum Live", category: "festival", color: "#fb7185", radius: 15, bpm: 126, genre: "Melodic Techno", description: "Sensory architectural livestream with Stephan Bodzin at the Roman Colosseum.", connections: ["art_stephanbodzin"] },
  { id: "gear_space_echo", name: "Roland Space Echo RE-201", category: "gear", color: "#84cc16", radius: 12, description: "Vintage 1974 analog magnetic tape loop delay unit defining Dub Techno and Nils Frahm.", connections: ["art_nilsfrahm", "city_berlin"] },
  { id: "ven_potsdam_fabrik", name: "Fabrik Potsdam Soundstage", category: "venue", color: "#eab308", radius: 13, description: "Industrial arts factory and acoustic live hall on the outskirts of Berlin.", connections: ["city_berlin"] },
  { id: "art_ar_rahman", name: "A.R. Rahman (Panchathan)", category: "artist", color: "#c084fc", radius: 15, bpm: 110, genre: "Soundtrack", description: "Academy Award maestro pioneering eastern-western cinematic synthesis.", connections: ["std_yrf_mumbai", "city_london"] },
];

export const D3ForceGraph: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const dispatch = useAppDispatch();

  // Dynamic D3 Graph State
  const [nodes, setNodes] = useState<D3Node[]>(INITIAL_D3_NODES);
  const [selectedNode, setSelectedNode] = useState<D3Node | null>(INITIAL_D3_NODES[0]);
  const [hoveredNode, setHoveredNode] = useState<D3Node | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Live Real-Time Expansion State
  const [isExpandingLive, setIsExpandingLive] = useState(true);
  const [expansionSpeed, setExpansionSpeed] = useState<number>(1);
  const [liveEpoch, setLiveEpoch] = useState<number>(428);
  const [edgeCount, setEdgeCount] = useState<number>(24007);
  const [recentSpawnToast, setRecentSpawnToast] = useState<string | null>("D3.js Force Simulation Active");

  // D3 References
  const simulationRef = useRef<d3.Simulation<D3Node, D3Link> | null>(null);
  const zoomBehaviorRef = useRef<d3.ZoomBehavior<SVGSVGElement, unknown> | null>(null);

  // Build Links from Current Nodes
  const generateLinks = (currentNodes: D3Node[]): D3Link[] => {
    const links: D3Link[] = [];
    const nodeMap = new Map(currentNodes.map((n) => [n.id, n]));
    const linkSet = new Set<string>();

    currentNodes.forEach((sourceNode) => {
      sourceNode.connections.forEach((targetId) => {
        if (nodeMap.has(targetId)) {
          const key = [sourceNode.id, targetId].sort().join("---");
          if (!linkSet.has(key)) {
            linkSet.add(key);
            links.push({
              source: sourceNode.id,
              target: targetId,
            });
          }
        }
      });
    });

    return links;
  };

  // Spawn New Node into D3 Graph
  const spawnD3Node = useCallback(() => {
    setNodes((prevNodes) => {
      const unspawned = DYNAMIC_INGESTION_POOL.filter(
        (cand) => !prevNodes.some((existing) => existing.id === cand.id)
      );

      let newNode: D3Node;
      if (unspawned.length > 0) {
        newNode = { ...unspawned[0], isNew: true };
      } else {
        const randId = `d3_dyn_hub_${Date.now().toString().slice(-4)}`;
        const parent = prevNodes[Math.floor(Math.random() * prevNodes.length)];
        newNode = {
          id: randId,
          name: `Recursive Micro-Hub #${randId.slice(-4)}`,
          category: "venue",
          color: "#eab308",
          radius: 13,
          description: `Autonomous satellite sub-hub spawned via recursive multi-hop wave propagation from ${parent.name}.`,
          connections: [parent.id],
          isNew: true,
        };
      }

      setLiveEpoch((prev) => prev + 1);
      setEdgeCount((prev) => prev + Math.floor(25 + Math.random() * 30));
      setRecentSpawnToast(`+ Ingested: ${newNode.name} (${newNode.category.toUpperCase()})`);

      return [...prevNodes, newNode];
    });
  }, []);

  // Continuous Auto-Expansion Interval Loop
  useEffect(() => {
    if (!isExpandingLive) return;
    const intervalMs = Math.max(1000, 3200 / expansionSpeed);
    const timer = setInterval(() => {
      spawnD3Node();
    }, intervalMs);

    return () => clearInterval(timer);
  }, [isExpandingLive, expansionSpeed, spawnD3Node]);

  // Initialize and Update D3.js Force Simulation
  useEffect(() => {
    if (!svgRef.current || !containerRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = containerRef.current.clientWidth || 900;
    const height = containerRef.current.clientHeight || 560;

    svg.attr("width", width).attr("height", height);

    // Clear previous elements
    svg.selectAll("*").remove();

    // 1. Defs: Glow Filters and Gradients
    const defs = svg.append("defs");

    // Glow Filter
    const filter = defs.append("filter").attr("id", "glow").attr("x", "-50%").attr("y", "-50%").attr("width", "200%").attr("height", "200%");
    filter.append("feGaussianBlur").attr("stdDeviation", "4").attr("result", "coloredBlur");
    const feMerge = filter.append("feMerge");
    feMerge.append("feMergeNode").attr("in", "coloredBlur");
    feMerge.append("feMergeNode").attr("in", "SourceGraphic");

    // 2. Main Zoomable Container Group
    const g = svg.append("g").attr("class", "d3-graph-content");

    // Zoom & Pan Behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.25, 4.0])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });

    svg.call(zoom);
    zoomBehaviorRef.current = zoom;

    // Center view
    svg.call(zoom.transform, d3.zoomIdentity.translate(width / 2, height / 2).scale(0.85));

    // 3. Prepare Links & Nodes Data
    const linksData = generateLinks(nodes);

    // 4. Create D3 Force Simulation
    const simulation = d3.forceSimulation<D3Node, D3Link>(nodes)
      .force("link", d3.forceLink<D3Node, D3Link>(linksData).id((d) => d.id).distance(80).strength(0.5))
      .force("charge", d3.forceManyBody().strength(-240))
      .force("center", d3.forceCenter(0, 0).strength(0.08))
      .force("collide", d3.forceCollide().radius((d: any) => (d.radius || 15) + 12).iterations(2))
      .alphaDecay(0.025);

    simulationRef.current = simulation;

    // 5. Draw Links (Glowing Green Laser Edges)
    const linkGroup = g.append("g").attr("class", "links");
    const linkElements = linkGroup.selectAll("line")
      .data(linksData)
      .enter()
      .append("line")
      .attr("stroke", "#1DB954")
      .attr("stroke-opacity", 0.35)
      .attr("stroke-width", 1.5)
      .attr("stroke-dasharray", "4,2");

    // 6. Draw Nodes Group
    const nodeGroup = g.append("g").attr("class", "nodes");
    const nodeElements = nodeGroup.selectAll("g")
      .data(nodes, (d: any) => d.id)
      .enter()
      .append("g")
      .attr("class", "node-item")
      .attr("cursor", "pointer");

    // Ripple Pulse Halo for New Nodes
    nodeElements.filter((d) => Boolean(d.isNew))
      .append("circle")
      .attr("r", (d) => d.radius)
      .attr("fill", "none")
      .attr("stroke", (d) => d.color)
      .attr("stroke-width", 2)
      .attr("opacity", 1)
      .transition()
      .duration(1200)
      .ease(d3.easeCircleOut)
      .attr("r", (d) => d.radius * 2.8)
      .attr("opacity", 0)
      .remove();

    // Node Outer Ring
    nodeElements.append("circle")
      .attr("r", (d) => d.radius + 3)
      .attr("fill", "none")
      .attr("stroke", (d) => d.color)
      .attr("stroke-width", 1.5)
      .attr("stroke-opacity", 0.6);

    // Node Main Solid Core
    nodeElements.append("circle")
      .attr("r", (d) => d.radius)
      .attr("fill", (d) => d.color)
      .attr("filter", "url(#glow)")
      .attr("fill-opacity", 0.85);

    // Node Label Text
    nodeElements.append("text")
      .text((d) => d.name)
      .attr("x", (d) => d.radius + 6)
      .attr("y", 4)
      .attr("fill", "#ffffff")
      .attr("font-size", "10px")
      .attr("font-family", "monospace")
      .attr("font-weight", "bold")
      .attr("opacity", 0.8)
      .attr("pointer-events", "none")
      .style("text-shadow", "0 2px 4px rgba(0,0,0,0.9)");

    // 7. Drag Interactions
    const drag = d3.drag<SVGGElement, D3Node>()
      .on("start", (event, d) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      })
      .on("drag", (event, d) => {
        d.fx = event.x;
        d.fy = event.y;
      })
      .on("end", (event, d) => {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      });

    nodeElements.call(drag as any);

    // 8. Hover & Click Event Handlers
    nodeElements
      .on("mouseenter", (event, d) => {
        setHoveredNode(d);
        d3.select(event.currentTarget).select("circle:nth-child(2)").attr("stroke-width", 3).attr("stroke-opacity", 1);
      })
      .on("mouseleave", (event, d) => {
        setHoveredNode(null);
        d3.select(event.currentTarget).select("circle:nth-child(2)").attr("stroke-width", 1.5).attr("stroke-opacity", 0.6);
      })
      .on("click", (event, d) => {
        event.stopPropagation();
        setSelectedNode(d);

        // Smoothly pan to clicked node
        svg.transition().duration(750).call(
          zoom.transform,
          d3.zoomIdentity.translate(width / 2 - (d.x || 0), height / 2 - (d.y || 0)).scale(1.2)
        );
      });

    // 9. Simulation Tick Update Loop
    simulation.on("tick", () => {
      linkElements
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);

      nodeElements.attr("transform", (d: any) => `translate(${d.x},${d.y})`);
    });

    return () => {
      simulation.stop();
    };
  }, [nodes]);

  // Zoom Controls
  const handleZoom = (factor: number) => {
    if (!svgRef.current || !zoomBehaviorRef.current) return;
    d3.select(svgRef.current).transition().duration(300).call(zoomBehaviorRef.current.scaleBy, factor);
  };

  const handleResetZoom = () => {
    if (!svgRef.current || !zoomBehaviorRef.current || !containerRef.current) return;
    const width = containerRef.current.clientWidth || 900;
    const height = containerRef.current.clientHeight || 560;
    d3.select(svgRef.current).transition().duration(600).call(
      zoomBehaviorRef.current.transform,
      d3.zoomIdentity.translate(width / 2, height / 2).scale(0.85)
    );
  };

  return (
    <div
      ref={containerRef}
      className={`relative w-full rounded-2xl overflow-hidden border border-white/10 bg-[#050508] transition-all ${
        isFullscreen ? "fixed inset-0 z-50 rounded-none h-screen" : "h-[560px] sm:h-[620px] shadow-2xl"
      }`}
    >
      {/* D3.js SVG Force Canvas */}
      <svg ref={svgRef} className="w-full h-full cursor-grab active:cursor-grabbing select-none" />

      {/* Top HUD: Real-Time Live Autonomous Expansion Beacon */}
      <div className="absolute top-4 left-4 right-4 flex flex-wrap justify-between items-center gap-3 pointer-events-none">
        <div className="flex items-center gap-3 bg-black/90 backdrop-blur-xl px-4 py-2 rounded-full border border-white/15 pointer-events-auto shadow-2xl">
          <div className="relative flex items-center justify-center">
            <span className={`w-3 h-3 rounded-full ${isExpandingLive ? "bg-[#1DB954]" : "bg-amber-400"}`}></span>
            {isExpandingLive && (
              <span className="absolute w-5 h-5 rounded-full bg-[#1DB954]/50 animate-ping"></span>
            )}
          </div>
          <div className="text-xs font-mono text-white">
            <span className="font-extrabold text-[#1DB954]">
              {isExpandingLive ? "D3.JS FORCE EXPANSION ACTIVE" : "EXPANSION PAUSED"}
            </span>
            <span className="text-white/40 mx-2">•</span>
            <span className="font-bold">EPOCH #{liveEpoch}</span>
            <span className="text-white/40 mx-2">•</span>
            <span>{nodes.length} NODES</span>
            <span className="text-white/40 mx-2">•</span>
            <span>{edgeCount.toLocaleString()} EDGES</span>
          </div>
        </div>

        {/* Live Expansion Controls */}
        <div className="flex items-center gap-2 pointer-events-auto">
          {/* Trigger Immediate Wave Button */}
          <button
            onClick={spawnD3Node}
            className="px-3 py-1.5 rounded-full text-xs font-mono font-bold bg-[#1DB954]/20 hover:bg-[#1DB954]/30 border border-[#1DB954]/50 text-[#1DB954] transition-all flex items-center gap-1.5 shadow-xl backdrop-blur-md"
            title="Immediately pulse and spawn new node into D3 force simulation"
          >
            <PlusCircle className="w-3.5 h-3.5" />
            <span>+ Pulse Node</span>
          </button>

          {/* Pause / Resume Live Stream */}
          <button
            onClick={() => setIsExpandingLive(!isExpandingLive)}
            className={`px-3 py-1.5 rounded-full text-xs font-mono font-bold border transition-all flex items-center gap-1.5 bg-black/85 backdrop-blur-md ${
              isExpandingLive ? "border-[#1DB954] text-[#1DB954]" : "border-amber-400 text-amber-400"
            }`}
          >
            {isExpandingLive ? (
              <>
                <Pause className="w-3.5 h-3.5" /> Pause
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-amber-400" /> Resume
              </>
            )}
          </button>

          {/* Zoom Buttons */}
          <button
            onClick={() => handleZoom(1.3)}
            className="w-8 h-8 rounded-full bg-black/85 backdrop-blur-md border border-white/10 flex items-center justify-center text-white hover:bg-white/10 transition-all shadow-xl"
            title="Zoom In"
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => handleZoom(0.7)}
            className="w-8 h-8 rounded-full bg-black/85 backdrop-blur-md border border-white/10 flex items-center justify-center text-white hover:bg-white/10 transition-all shadow-xl"
            title="Zoom Out"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={handleResetZoom}
            className="w-8 h-8 rounded-full bg-black/85 backdrop-blur-md border border-white/10 flex items-center justify-center text-white hover:bg-white/10 transition-all shadow-xl"
            title="Reset Zoom & Center"
          >
            <Compass className="w-3.5 h-3.5" />
          </button>

          {/* Fullscreen Toggle */}
          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="w-8 h-8 rounded-full bg-black/85 backdrop-blur-md border border-white/10 flex items-center justify-center text-white hover:bg-white/10 transition-all shadow-2xl"
          >
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Real-Time Live Ticker Toast */}
      {recentSpawnToast && (
        <div className="absolute top-16 left-4 bg-black/90 backdrop-blur-md border border-[#1DB954]/40 px-3.5 py-1.5 rounded-full text-xs font-mono text-[#1DB954] shadow-2xl flex items-center gap-2 pointer-events-none animate-in fade-in slide-in-from-top-2 duration-200">
          <Activity className="w-3.5 h-3.5 animate-pulse text-[#1DB954]" />
          <span>{recentSpawnToast}</span>
        </div>
      )}

      {/* Floating Hover Label Pill */}
      {hoveredNode && !selectedNode && (
        <div className="absolute top-28 left-1/2 -translate-x-1/2 bg-black/90 backdrop-blur-md border border-[#1DB954]/40 px-3.5 py-1 rounded-full text-xs font-mono text-white shadow-2xl flex items-center gap-2 pointer-events-none animate-in fade-in duration-150">
          <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: hoveredNode.color }}></span>
          <span className="font-bold">{hoveredNode.name}</span>
          <span className="text-white/40 uppercase text-[10px]">({hoveredNode.category})</span>
        </div>
      )}

      {/* Bottom Floating Inspector HUD */}
      {selectedNode && (
        <div className="absolute bottom-4 left-4 right-4 sm:right-auto sm:max-w-md bg-[#121212]/95 backdrop-blur-xl border border-white/10 p-5 rounded-2xl shadow-2xl space-y-3 animate-in fade-in slide-in-from-bottom-4 duration-300">
          <div className="flex justify-between items-start">
            <div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: selectedNode.color }}></span>
                <span className="font-extrabold text-sm text-white">{selectedNode.name}</span>
                <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-white/10 text-white font-bold">
                  {selectedNode.category}
                </span>
              </div>
              {selectedNode.country && (
                <div className="text-xs text-[#b3b3b3] mt-0.5">{selectedNode.country}</div>
              )}
            </div>
            {selectedNode.bpm && (
              <span className="text-[11px] font-mono text-[#1DB954] font-bold px-2 py-0.5 rounded bg-[#1DB954]/10 border border-[#1DB954]/30">
                {selectedNode.bpm} BPM
              </span>
            )}
          </div>

          <p className="text-xs text-slate-300 leading-relaxed">{selectedNode.description}</p>

          {selectedNode.soundSystem && (
            <div className="p-2.5 bg-black/60 rounded-xl border border-white/5 text-[11px] font-mono text-white/80">
              <span className="text-white/40 block text-[9px] uppercase font-bold">
                Sound System & Acoustic Specs
              </span>
              {selectedNode.soundSystem}
            </div>
          )}

          <div className="flex items-center justify-between pt-1 border-t border-white/5">
            <div className="text-[10px] font-mono text-white/50">
              Corridor Connections: <span className="text-white font-bold">{selectedNode.connections.length} Links</span>
            </div>
            {selectedNode.category === "artist" && (
              <button
                onClick={() => {
                  dispatch(
                    setTrack({
                      title: `${selectedNode.name} - Benchmark Cut`,
                      artist: selectedNode.name,
                      genre: selectedNode.genre || "Electronic",
                      bpm: selectedNode.bpm || 126,
                      duration: "6:30",
                    })
                  );
                  dispatch(setIsPlaying(true));
                }}
                className="px-3.5 py-1.5 bg-[#1DB954] hover:bg-[#1ed760] text-black font-extrabold rounded-full text-xs flex items-center gap-1.5 shadow-md shadow-[#1DB954]/20"
              >
                <Play className="w-3.5 h-3.5 fill-black" /> Benchmark Playback
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
