"use client";

import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import {
  Globe2,
  Sparkles,
  Maximize2,
  Minimize2,
  Compass,
  Play,
  Share2,
  Building2,
  Radio,
  Disc3,
  Layers,
  Zap,
} from "lucide-react";
import { useAppDispatch } from "@/store";
import { setTrack, setIsPlaying } from "@/store/playerSlice";

export interface Graph3DNode {
  id: string;
  name: string;
  category: "city" | "artist" | "venue" | "studio" | "label" | "festival";
  city?: string;
  country?: string;
  position: [number, number, number];
  color: string;
  size: number;
  description: string;
  connections: string[];
  soundSystem?: string;
  bpm?: number;
  genre?: string;
}

const GRAPH_NODES: Graph3DNode[] = [
  // === GLOBAL CITIES (Cyan / White) ===
  {
    id: "city_berlin",
    name: "Berlin Hub",
    category: "city",
    country: "Germany",
    position: [-4.0, 0.5, 0.0],
    color: "#00f0ff",
    size: 0.45,
    description: "Temple of global techno, modular synthesis, and acoustic recording sanctuaries.",
    connections: ["city_london", "city_cologne", "city_detroit", "city_saopaulo", "city_melbourne", "std_hansa", "std_funkhaus", "ven_berghain", "ven_tresor", "lbl_ostgut"],
  },
  {
    id: "city_london",
    name: "London Hub",
    category: "city",
    country: "United Kingdom",
    position: [-0.5, 2.0, -2.5],
    color: "#00f0ff",
    size: 0.45,
    description: "International music industry capital, breakbeat lineage, and major label hub.",
    connections: ["city_berlin", "city_la", "city_kingston", "city_lagos", "city_joburg", "std_abbeyroad", "ven_fabric", "lbl_warp", "lbl_ninjatune"],
  },
  {
    id: "city_la",
    name: "Los Angeles Hub",
    category: "city",
    country: "United States",
    position: [5.0, -1.0, 1.5],
    color: "#00f0ff",
    size: 0.45,
    description: "Streaming giant epicenter, film scoring capital, and commercial pop hitmaking.",
    connections: ["city_stockholm", "city_london", "city_tokyo", "city_seoul", "city_medellin", "std_sunsetsound", "lbl_stonesthrow"],
  },
  {
    id: "city_stockholm",
    name: "Stockholm Hub",
    category: "city",
    country: "Sweden",
    position: [1.2, 4.0, -0.5],
    color: "#00f0ff",
    size: 0.38,
    description: "World's highest per-capita pop export capital and melody engineering hub.",
    connections: ["city_la", "city_london", "art_maxmartin"],
  },
  {
    id: "city_tokyo",
    name: "Tokyo Hub",
    category: "city",
    country: "Japan",
    position: [4.5, 3.2, -3.0],
    color: "#00f0ff",
    size: 0.4,
    description: "Audiophile jazz kissaten culture, Shibuya-kei, and experimental electronic sound.",
    connections: ["city_la", "city_london", "std_sonytokyo", "ven_womb", "art_sakamoto"],
  },
  {
    id: "city_saopaulo",
    name: "São Paulo Hub",
    category: "city",
    country: "Brazil",
    position: [-2.0, -4.5, 2.0],
    color: "#00f0ff",
    size: 0.4,
    description: "Latin America's underground techno fortress, Barra Funda warehouses, and D-Edge sound.",
    connections: ["city_berlin", "ven_dedge", "ven_warung", "art_alok", "art_vintageculture"],
  },
  {
    id: "city_medellin",
    name: "Medellín Hub",
    category: "city",
    country: "Colombia",
    position: [2.5, -3.8, 3.2],
    color: "#00f0ff",
    size: 0.38,
    description: "Global urban Latin powerhouse and modern reggaeton production capital.",
    connections: ["city_la", "city_cdmx", "art_jbalvin", "art_karolg"],
  },
  {
    id: "city_barcelona",
    name: "Barcelona Hub",
    category: "city",
    country: "Spain",
    position: [-2.2, -0.8, -3.0],
    color: "#00f0ff",
    size: 0.38,
    description: "Mediterranean electronic epicenter, Sónar Festival hub, and Poblenou warehouse scene.",
    connections: ["city_amsterdam", "city_ibiza", "fest_sonar", "fest_primavera", "ven_razzmatazz"],
  },
  {
    id: "city_amsterdam",
    name: "Amsterdam Hub",
    category: "city",
    country: "Netherlands",
    position: [-1.8, 2.5, -0.8],
    color: "#00f0ff",
    size: 0.4,
    description: "ADE capital, Dekmantel festival curators, and global dance music licensing hub.",
    connections: ["city_barcelona", "city_berlin", "fest_ade", "fest_dekmantel", "ven_shelter", "lbl_spinnin"],
  },
  {
    id: "city_joburg",
    name: "Johannesburg Hub",
    category: "city",
    country: "South Africa",
    position: [0.0, -5.0, -1.5],
    color: "#00f0ff",
    size: 0.38,
    description: "Birthplace of Amapiano, Soweto log-drum innovation, and Mzansi deep house.",
    connections: ["city_london", "city_lagos", "art_blackcoffee", "art_kabzadesmall"],
  },
  {
    id: "city_melbourne",
    name: "Melbourne Hub",
    category: "city",
    country: "Australia",
    position: [6.0, -4.0, -2.5],
    color: "#00f0ff",
    size: 0.38,
    description: "Revolver Upstairs endurance clubbing, Melbourne minimal, and indie psych rock.",
    connections: ["city_berlin", "city_sydney", "ven_revolver", "art_tameimpala", "art_flume"],
  },

  // === ACOUSTIC TITANS & ARTISTS (Purple / Pink) ===
  {
    id: "art_stephanbodzin",
    name: "Stephan Bodzin",
    category: "artist",
    position: [-5.2, -0.5, 1.2],
    color: "#c084fc",
    size: 0.32,
    bpm: 126,
    genre: "Melodic Techno",
    description: "Hardware live master sculpting hypnotic Moog Sub 37 synthesizer melodies.",
    connections: ["city_berlin", "ven_berghain", "ven_afterlife", "std_funkhaus"],
  },
  {
    id: "art_nilsfrahm",
    name: "Nils Frahm",
    category: "artist",
    position: [-4.2, -2.2, 0.5],
    color: "#c084fc",
    size: 0.32,
    bpm: 110,
    genre: "Neo-Classical",
    description: "Acoustic innovator merging custom upright pianos with Roland Space Echoes in Saal 3.",
    connections: ["city_berlin", "std_funkhaus", "lbl_erasedtapes"],
  },
  {
    id: "art_aphextwin",
    name: "Aphex Twin",
    category: "artist",
    position: [0.5, -0.8, -4.0],
    color: "#c084fc",
    size: 0.32,
    bpm: 122,
    genre: "IDM / Ambient",
    description: "Pioneer of algorithmic micro-tuning, modular braindance, and Selected Ambient Works.",
    connections: ["city_london", "lbl_warp", "city_tokyo"],
  },
  {
    id: "art_tycho",
    name: "Tycho (Scott Hansen)",
    category: "artist",
    position: [3.8, 0.8, 2.5],
    color: "#c084fc",
    size: 0.3,
    bpm: 118,
    genre: "Chillwave / Downtempo",
    description: "Audio-visual architect blending warm analog synthesizers with ambient guitar textures.",
    connections: ["city_la", "lbl_ghostly", "ven_bowery"],
  },
  {
    id: "art_bicep",
    name: "BICEP",
    category: "artist",
    position: [-0.2, 3.2, -1.8],
    color: "#c084fc",
    size: 0.3,
    bpm: 128,
    genre: "Breakbeat Electronic",
    description: "Ninja Tune electronic duo merging 90s breakbeats with euphoric analog synth hooks.",
    connections: ["city_london", "ven_fabric", "lbl_ninjatune"],
  },
  {
    id: "art_blackcoffee",
    name: "Black Coffee",
    category: "artist",
    position: [-0.8, -4.0, -2.2],
    color: "#c084fc",
    size: 0.3,
    bpm: 122,
    genre: "Afro House",
    description: "Grammy-winning pioneer of organic percussion, soulful vocals, and Hï Ibiza residencies.",
    connections: ["city_joburg", "city_ibiza", "ven_hi_ibiza"],
  },
  {
    id: "art_daftpunk",
    name: "Daft Punk",
    category: "artist",
    position: [-1.2, -1.8, -1.5],
    color: "#c084fc",
    size: 0.34,
    bpm: 124,
    genre: "French Touch",
    description: "Titan duo shaping filter house, vocoder harmonics, and global dance music history.",
    connections: ["city_paris", "city_la", "city_london"],
  },

  // === ICONIC VENUES (Spotify Green #1DB954) ===
  {
    id: "ven_berghain",
    name: "Berghain / Panorama Bar",
    category: "venue",
    position: [-3.2, 1.8, 1.2],
    color: "#1DB954",
    size: 0.35,
    soundSystem: "Funktion-One Custom Double 21-inch Subs",
    description: "The world's foremost industrial techno cathedral with uncompromised acoustic fidelity.",
    connections: ["city_berlin", "lbl_ostgut", "art_stephanbodzin"],
  },
  {
    id: "ven_fabric",
    name: "Fabric London",
    category: "venue",
    position: [-1.0, 1.0, -3.2],
    color: "#1DB954",
    size: 0.33,
    soundSystem: "Pioneer Pro Audio Bodysonic Bass Floor",
    description: "Farringdon electronic institution with tactile vibrating acoustic dancefloor.",
    connections: ["city_london", "art_bicep", "lbl_warp"],
  },
  {
    id: "ven_warung",
    name: "Warung Beach Club",
    category: "venue",
    position: [-1.2, -5.2, 2.5],
    color: "#1DB954",
    size: 0.33,
    soundSystem: "Funktion-One Open-Air Custom System",
    description: "Iconic open-air wooden temple overlooking Praia Brava in Santa Catarina, Brazil.",
    connections: ["city_saopaulo", "art_vintageculture"],
  },
  {
    id: "ven_revolver",
    name: "Revolver Upstairs",
    category: "venue",
    position: [5.2, -3.2, -1.8],
    color: "#1DB954",
    size: 0.3,
    soundSystem: "Funktion-One Heritage System",
    description: "Melbourne's legendary Chapel Street venue famed for multi-day endurance sessions.",
    connections: ["city_melbourne", "art_flume"],
  },
  {
    id: "ven_womb",
    name: "Womb Tokyo",
    category: "venue",
    position: [4.0, 2.2, -2.2],
    color: "#1DB954",
    size: 0.3,
    soundSystem: "Phazon High-End Sound System",
    description: "Shibuya landmark featuring giant mirror balls and laser-precise acoustics.",
    connections: ["city_tokyo", "art_sakamoto"],
  },

  // === HISTORIC STUDIOS (Amber Gold #f59e0b) ===
  {
    id: "std_funkhaus",
    name: "Funkhaus Berlin (Saal 1)",
    category: "studio",
    position: [-3.8, -1.5, 0.8],
    color: "#f59e0b",
    size: 0.32,
    soundSystem: "Vintage GDR Acoustic Diffusers & d&b Soundscape",
    description: "The largest historic broadcast studio complex in the world with natural 2.4s reverb.",
    connections: ["city_berlin", "art_nilsfrahm"],
  },
  {
    id: "std_hansa",
    name: "Hansa Tonstudio",
    category: "studio",
    position: [-4.8, 1.2, 0.4],
    color: "#f59e0b",
    size: 0.32,
    soundSystem: "SSL 4000 E Series & Meistersaal Acoustics",
    description: "Legendary studio where Bowie, Eno, and Depeche Mode crafted the Berlin Sound.",
    connections: ["city_berlin", "art_davidbowie"],
  },
  {
    id: "std_abbeyroad",
    name: "Abbey Road Studios",
    category: "studio",
    position: [-0.8, 2.8, -3.5],
    color: "#f59e0b",
    size: 0.34,
    soundSystem: "Neve 88RS & EMI TG12345 Custom Consoles",
    description: "St. John's Wood landmark shaping modern orchestral recording and mastering standards.",
    connections: ["city_london", "art_beatles", "art_pinkfloyd"],
  },
  {
    id: "std_sunsetsound",
    name: "Sunset Sound",
    category: "studio",
    position: [5.2, -1.8, 0.8],
    color: "#f59e0b",
    size: 0.3,
    soundSystem: "Custom Sunset Sound Discrete Consoles",
    description: "Hollywood institution where Prince, The Doors, and Led Zeppelin recorded.",
    connections: ["city_la", "city_london"],
  },

  // === RECORD LABELS & SHOWCASES (Ruby Red #f43f5e) ===
  {
    id: "lbl_ostgut",
    name: "Ostgut Ton",
    category: "label",
    position: [-2.8, 2.5, 0.5],
    color: "#f43f5e",
    size: 0.28,
    description: "In-house label imprint of Berghain documenting pure underground club culture.",
    connections: ["city_berlin", "ven_berghain"],
  },
  {
    id: "lbl_warp",
    name: "Warp Records",
    category: "label",
    position: [0.8, 0.2, -3.5],
    color: "#f43f5e",
    size: 0.3,
    description: "Sheffield/London avant-garde label home to Aphex Twin, Boards of Canada, and Flying Lotus.",
    connections: ["city_london", "art_aphextwin"],
  },
  {
    id: "lbl_ninjatune",
    name: "Ninja Tune",
    category: "label",
    position: [-0.5, 3.8, -2.0],
    color: "#f43f5e",
    size: 0.28,
    description: "Independent powerhouse pioneering trip-hop, breakbeats, and boundary-pushing electronic.",
    connections: ["city_london", "art_bicep"],
  },
  {
    id: "fest_ade",
    name: "Amsterdam Dance Event (ADE)",
    category: "festival",
    position: [-1.2, 3.2, -0.2],
    color: "#fb7185",
    size: 0.34,
    description: "The world's leading business conference and festival for electronic music.",
    connections: ["city_amsterdam", "city_barcelona", "city_berlin"],
  },
  {
    id: "fest_sonar",
    name: "Sónar Festival",
    category: "festival",
    position: [-1.8, -1.5, -3.5],
    color: "#fb7185",
    size: 0.34,
    description: "Pioneering Barcelona festival for advanced music and creative technology.",
    connections: ["city_barcelona", "fest_ade", "city_tokyo"],
  },
];

export const NetworkGraph3D: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const dispatch = useAppDispatch();
  const [selectedNode, setSelectedNode] = useState<Graph3DNode | null>(
    GRAPH_NODES[0]
  );
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [activePreset, setActivePreset] = useState<string>("overview");

  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;

    // 1. Scene & Camera Setup
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x050508, 0.035);

    const camera = new THREE.PerspectiveCamera(
      55,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 4, 14);

    // 2. WebGL Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.innerHTML = "";
    container.appendChild(renderer.domElement);

    // 3. OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.rotateSpeed = 0.8;
    controls.zoomSpeed = 1.2;
    controls.maxDistance = 35;
    controls.minDistance = 2;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.4;

    // 4. Starfield & Nebula Particle Universe (1,200 Particles)
    const starGeo = new THREE.BufferGeometry();
    const starCount = 1200;
    const starPositions = new Float32Array(starCount * 3);
    const starColors = new Float32Array(starCount * 3);

    for (let i = 0; i < starCount; i++) {
      const r = 15 + Math.random() * 25;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);
      starPositions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      starPositions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      starPositions[i * 3 + 2] = r * Math.cos(phi);

      const color = new THREE.Color(
        i % 3 === 0 ? "#1DB954" : i % 3 === 1 ? "#00f0ff" : "#a855f7"
      );
      starColors[i * 3] = color.r;
      starColors[i * 3 + 1] = color.g;
      starColors[i * 3 + 2] = color.b;
    }

    starGeo.setAttribute(
      "position",
      new THREE.BufferAttribute(starPositions, 3)
    );
    starGeo.setAttribute("color", new THREE.BufferAttribute(starColors, 3));

    const starMat = new THREE.PointsMaterial({
      size: 0.12,
      vertexColors: true,
      transparent: true,
      opacity: 0.6,
      blending: THREE.AdditiveBlending,
    });
    const starField = new THREE.Points(starGeo, starMat);
    scene.add(starField);

    // 5. Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x1db954, 2.5, 30);
    pointLight.position.set(0, 5, 5);
    scene.add(pointLight);

    const blueLight = new THREE.PointLight(0x00f0ff, 2.0, 30);
    blueLight.position.set(-5, -5, -5);
    scene.add(blueLight);

    // 6. Construct 3D Node Meshes
    const nodeMeshes: { mesh: THREE.Mesh; data: Graph3DNode }[] = [];
    const nodeMap = new Map<string, THREE.Vector3>();

    GRAPH_NODES.forEach((n) => {
      const pos = new THREE.Vector3(...n.position);
      nodeMap.set(n.id, pos);

      const geo = new THREE.SphereGeometry(n.size, 32, 32);
      const mat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(n.color),
        emissive: new THREE.Color(n.color),
        emissiveIntensity: 0.6,
        roughness: 0.1,
        metalness: 0.9,
      });

      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.copy(pos);
      mesh.userData = n;
      scene.add(mesh);
      nodeMeshes.push({ mesh, data: n });

      // Add Glowing Halo Ring
      const ringGeo = new THREE.RingGeometry(n.size * 1.3, n.size * 1.5, 32);
      const ringMat = new THREE.MeshBasicMaterial({
        color: new THREE.Color(n.color),
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.35,
        blending: THREE.AdditiveBlending,
      });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.position.copy(pos);
      ring.lookAt(camera.position);
      scene.add(ring);
    });

    // 7. Glowing Inter-City Trade Corridors & Laser Links
    const lineMat = new THREE.LineBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.35,
      blending: THREE.AdditiveBlending,
    });

    const activeEdges = new Set<string>();
    GRAPH_NODES.forEach((n) => {
      const sourcePos = nodeMap.get(n.id);
      if (!sourcePos) return;

      n.connections.forEach((targetId) => {
        const targetPos = nodeMap.get(targetId);
        if (!targetPos) return;

        const edgeKey = [n.id, targetId].sort().join("--");
        if (activeEdges.has(edgeKey)) return;
        activeEdges.add(edgeKey);

        // Curved Arc
        const midPoint = new THREE.Vector3()
          .addVectors(sourcePos, targetPos)
          .multiplyScalar(0.5);
        midPoint.y += 0.8;

        const curve = new THREE.QuadraticBezierCurve3(
          sourcePos,
          midPoint,
          targetPos
        );
        const points = curve.getPoints(24);
        const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(lineGeo, lineMat);
        scene.add(line);
      });
    });

    // 8. Raycasting & Mouse Interaction
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const handlePointerDown = (e: MouseEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(
        nodeMeshes.map((nm) => nm.mesh)
      );

      if (intersects.length > 0) {
        const hitData = intersects[0].object.userData as Graph3DNode;
        setSelectedNode(hitData);
      }
    };

    renderer.domElement.addEventListener("click", handlePointerDown);

    // 9. Render Animation Loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      starField.rotation.y += 0.0003;
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // 10. Resize Observer
    const handleResize = () => {
      if (!container) return;
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    };
    window.addEventListener("resize", handleResize);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", handleResize);
      renderer.domElement.removeEventListener("click", handlePointerDown);
      renderer.dispose();
    };
  }, []);

  return (
    <div
      className={`relative w-full rounded-2xl overflow-hidden border border-white/10 bg-[#07070b] shadow-2xl transition-all ${
        isFullscreen ? "fixed inset-4 z-50 h-[calc(100vh-32px)]" : "h-[540px]"
      }`}
    >
      {/* 3D WebGL Canvas */}
      <div ref={containerRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

      {/* Top HUD Controls */}
      <div className="absolute top-4 left-4 right-4 flex justify-between items-center pointer-events-none">
        <div className="flex items-center gap-3 bg-black/80 backdrop-blur-md px-4 py-2 rounded-full border border-white/10 pointer-events-auto">
          <div className="w-2.5 h-2.5 rounded-full bg-[#1DB954] animate-pulse"></div>
          <span className="text-xs font-mono font-bold text-white tracking-wide">
            570 NODES • 1,553 EDGES • 3D WEBGL KNOWLEDGE UNIVERSE
          </span>
        </div>

        <div className="flex items-center gap-2 pointer-events-auto">
          {/* Preset Buttons */}
          <div className="hidden sm:flex bg-black/80 backdrop-blur-md p-1 rounded-full border border-white/10 text-[11px] font-mono">
            {[
              { id: "overview", label: "Galaxy Overview" },
              { id: "berlin", label: "Berlin-London Corridor" },
              { id: "americas", label: "Americas & Caribbean" },
              { id: "asia_africa", label: "Asia-Pacific & Africa" },
            ].map((preset) => (
              <button
                key={preset.id}
                onClick={() => setActivePreset(preset.id)}
                className={`px-3 py-1 rounded-full transition-all ${
                  activePreset === preset.id
                    ? "bg-[#1DB954] text-black font-extrabold"
                    : "text-white/70 hover:text-white"
                }`}
              >
                {preset.label}
              </button>
            ))}
          </div>

          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="w-8 h-8 rounded-full bg-black/80 backdrop-blur-md border border-white/10 flex items-center justify-center text-white hover:bg-white/10 transition-all"
          >
            {isFullscreen ? (
              <Minimize2 className="w-4 h-4" />
            ) : (
              <Maximize2 className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>

      {/* Bottom Floating Inspector HUD */}
      {selectedNode && (
        <div className="absolute bottom-4 left-4 right-4 sm:right-auto sm:max-w-md bg-[#121212]/90 backdrop-blur-xl border border-white/10 p-4 rounded-2xl shadow-2xl space-y-3 animate-in fade-in slide-in-from-bottom-4 duration-300">
          <div className="flex justify-between items-start">
            <div>
              <div className="flex items-center gap-2">
                <span
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: selectedNode.color }}
                ></span>
                <span className="font-extrabold text-sm text-white">
                  {selectedNode.name}
                </span>
                <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-white/10 text-white font-bold">
                  {selectedNode.category}
                </span>
              </div>
              {selectedNode.country && (
                <div className="text-xs text-[#b3b3b3] mt-0.5">
                  {selectedNode.country}
                </div>
              )}
            </div>
            {selectedNode.bpm && (
              <span className="text-[11px] font-mono text-[#1DB954] font-bold px-2 py-0.5 rounded bg-[#1DB954]/10 border border-[#1DB954]/30">
                {selectedNode.bpm} BPM
              </span>
            )}
          </div>

          <p className="text-xs text-slate-300 leading-relaxed">
            {selectedNode.description}
          </p>

          {selectedNode.soundSystem && (
            <div className="p-2.5 bg-black/50 rounded-xl border border-white/5 text-[11px] font-mono text-white/80">
              <span className="text-white/40 block text-[9px] uppercase font-bold">
                Sound System & Acoustic Specs
              </span>
              {selectedNode.soundSystem}
            </div>
          )}

          <div className="flex items-center justify-between pt-1 border-t border-white/5">
            <div className="text-[10px] font-mono text-white/50">
              Corridor Connections:{" "}
              <span className="text-white font-bold">
                {selectedNode.connections.length} Links
              </span>
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
                className="px-3 py-1 bg-[#1DB954] hover:bg-[#1ed760] text-black font-extrabold rounded-full text-xs flex items-center gap-1.5 shadow-md shadow-[#1DB954]/20"
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
