"use client";

import React, { useEffect, useRef, useState, useCallback } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
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
  Radio,
  PlusCircle,
  FastForward,
} from "lucide-react";
import { useAppDispatch } from "@/store";
import { setTrack, setIsPlaying } from "@/store/playerSlice";

export interface Graph3DNode {
  id: string;
  name: string;
  category: "city" | "artist" | "venue" | "studio" | "label" | "festival" | "gear" | "genre";
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
  epochSpawned?: number;
}

// Initial Base Seed Nodes
const INITIAL_GRAPH_NODES: Graph3DNode[] = [
  // === GLOBAL CITIES (Cyan #00f0ff) ===
  {
    id: "city_berlin",
    name: "Berlin Hub",
    category: "city",
    country: "Germany",
    position: [-4.0, 0.5, 0.0],
    color: "#00f0ff",
    size: 0.45,
    description: "Temple of global techno, modular synthesis, and acoustic recording sanctuaries.",
    connections: ["city_london", "city_cologne", "city_saopaulo", "std_hansa", "std_funkhaus", "ven_berghain", "ven_tresor", "lbl_ostgut"],
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
    connections: ["city_berlin", "city_la", "city_mumbai", "std_abbeyroad", "ven_fabric", "lbl_warp"],
  },
  {
    id: "city_mumbai",
    name: "Mumbai Hub",
    category: "city",
    country: "India",
    position: [3.5, 0.5, 3.8],
    color: "#00f0ff",
    size: 0.45,
    description: "National commercial, hip-hop, and electronic capital (antiSOCIAL, YRF Studios, Azadi Records).",
    connections: ["city_london", "city_goa", "ven_antisocial_mumbai", "std_yrf_mumbai", "art_divine"],
  },
  {
    id: "city_goa",
    name: "Goa Coastal Hub",
    category: "city",
    country: "India",
    position: [4.5, -1.2, 4.5],
    color: "#00f0ff",
    size: 0.42,
    description: "Global spiritual capital of Goa Trance & coastal sunset deep house (HillTop, Shiva Valley, Anjuna).",
    connections: ["city_mumbai", "city_berlin", "ven_hilltop_goa", "cur_anjuna_goa"],
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
    connections: ["city_london", "city_tokyo", "std_sunsetsound"],
  },
  {
    id: "city_tokyo",
    name: "Tokyo Hub",
    category: "city",
    country: "Japan",
    position: [4.5, 3.2, -3.0],
    color: "#00f0ff",
    size: 0.42,
    description: "Audiophile jazz kissaten culture, Shibuya-kei, and experimental electronic sound.",
    connections: ["city_la", "city_london", "ven_womb"],
  },
  {
    id: "city_saopaulo",
    name: "São Paulo Hub",
    category: "city",
    country: "Brazil",
    position: [-2.0, -4.5, 2.0],
    color: "#00f0ff",
    size: 0.42,
    description: "Latin America's underground techno fortress, Barra Funda warehouses, and D-Edge sound.",
    connections: ["city_berlin", "ven_warung"],
  },
  {
    id: "city_barcelona",
    name: "Barcelona Hub",
    category: "city",
    country: "Spain",
    position: [-2.2, -0.8, -3.0],
    color: "#00f0ff",
    size: 0.4,
    description: "Mediterranean electronic epicenter, Sónar Festival hub, and Poblenou warehouse scene.",
    connections: ["city_berlin", "city_ibiza", "fest_sonar"],
  },

  // === VENUES (Gold #eab308) ===
  {
    id: "ven_berghain",
    name: "Berghain / Panorama Bar",
    category: "venue",
    position: [-4.5, 1.8, 0.8],
    color: "#eab308",
    size: 0.35,
    soundSystem: "Funktion-One Custom 4-Way Array",
    description: "Former GDR heating plant turned world capital of hedonistic industrial techno.",
    connections: ["city_berlin", "lbl_ostgut"],
  },
  {
    id: "ven_antisocial_mumbai",
    name: "antiSOCIAL Mumbai",
    category: "venue",
    position: [3.2, 1.2, 3.2],
    color: "#eab308",
    size: 0.32,
    soundSystem: "Subterranean Todi Mills Club PA",
    description: "Underground warehouse bunker for cutting-edge techno, modular live sets, and hip-hop cyphers.",
    connections: ["city_mumbai", "art_divine"],
  },
  {
    id: "ven_hilltop_goa",
    name: "HillTop Goa (Vagator)",
    category: "venue",
    position: [4.8, -0.8, 5.0],
    color: "#eab308",
    size: 0.34,
    soundSystem: "Full-Spectrum Open-Air Psychoacoustic Array",
    description: "The global spiritual mecca of Goa trance perched on Vagator's hills since the early 1980s.",
    connections: ["city_goa", "cur_anjuna_goa"],
  },
  {
    id: "ven_warung",
    name: "Warung Beach Club",
    category: "venue",
    position: [-2.5, -5.2, 2.5],
    color: "#eab308",
    size: 0.32,
    soundSystem: "Funktion-One Wooden Temple Rig",
    description: "Open-air temple in Praia Brava surrounded by the Atlantic rainforest.",
    connections: ["city_saopaulo"],
  },

  // === ARTISTS (Purple #c084fc) ===
  {
    id: "art_divine",
    name: "DIVINE (Gully Gang)",
    category: "artist",
    position: [3.8, 1.8, 3.9],
    color: "#c084fc",
    size: 0.34,
    bpm: 135,
    genre: "Gully Rap",
    description: "Pioneer of Mumbai's street hip-hop revolution signed to Mass Appeal India.",
    connections: ["city_mumbai", "ven_antisocial_mumbai"],
  },
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
    connections: ["city_berlin", "ven_berghain", "std_funkhaus"],
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
    description: "Acoustic innovator merging custom upright pianos with Roland Space Echoes.",
    connections: ["city_berlin", "std_funkhaus"],
  },

  // === CURATORS & FESTIVALS (Rose #fb7185) ===
  {
    id: "cur_anjuna_goa",
    name: "Anjunadeep Open Air Goa",
    category: "festival",
    position: [5.2, -1.8, 4.2],
    color: "#fb7185",
    size: 0.34,
    bpm: 123,
    genre: "Melodic House",
    description: "Anjuna beachfront showcase blending analog Prophet-6 pad swells with sunset melodic deep house.",
    connections: ["city_goa", "ven_hilltop_goa", "art_nilsfrahm"],
  },
  {
    id: "cur_boiler_room_mumbai",
    name: "Boiler Room Mumbai",
    category: "festival",
    position: [2.8, 0.2, 4.2],
    color: "#fb7185",
    size: 0.32,
    bpm: 135,
    genre: "Gully Bass",
    description: "Global underground livestream documenting authentic Mumbai street cyphers.",
    connections: ["city_mumbai", "art_divine"],
  },
  {
    id: "fest_sonar",
    name: "Sónar+D Barcelona",
    category: "festival",
    position: [-1.8, -1.5, -3.5],
    color: "#fb7185",
    size: 0.34,
    description: "Pioneering Barcelona congress for advanced electronic music and AI creative tech.",
    connections: ["city_barcelona", "city_tokyo"],
  },
];

// Continuous Stream Expansion Pool for Dynamic Spawning
const DYNAMIC_EXPANSION_POOL: Omit<Graph3DNode, "position">[] = [
  { id: "ven_rso_berlin", name: "RSO.BERLIN (Schöneweide)", category: "venue", color: "#eab308", size: 0.3, description: "Raw industrial warehouse bunker and home to Herrensauna marathon sessions.", connections: ["city_berlin", "coll_herrensauna"] },
  { id: "coll_herrensauna", name: "Herrensauna Collective", category: "artist", color: "#c084fc", size: 0.32, bpm: 148, genre: "Industrial Techno", description: "148+ BPM relentless fast techno brotherhood founded by CEM and MCMLXXXV.", connections: ["ven_rso_berlin", "city_berlin"] },
  { id: "std_yrf_mumbai", name: "YRF Studios (Andheri West)", category: "studio", color: "#38bdf8", size: 0.3, description: "Dolby Atmos Premier scoring stages and SSL Duality mixing consoles.", connections: ["city_mumbai"] },
  { id: "lbl_azadi", name: "Azadi Records", category: "label", color: "#f43f5e", size: 0.3, description: "Pioneering South Asian socio-political hip-hop label (Seedhe Maut, Prabh Deep).", connections: ["city_mumbai", "city_delhi"] },
  { id: "city_delhi", name: "New Delhi Hub", category: "city", color: "#00f0ff", size: 0.4, description: "Northern hip-hop, live jazz cabaret, and Magnetic Fields festival axis.", connections: ["city_mumbai", "lbl_azadi"] },
  { id: "subg_amapiano", name: "Amapiano (Soweto Log-Drum)", category: "genre", color: "#a855f7", size: 0.32, bpm: 114, genre: "House", description: "South African viral movement driven by FM log-drum sub-basslines and airy jazz keys.", connections: ["city_joburg", "art_blackcoffee"] },
  { id: "city_joburg", name: "Johannesburg Hub", category: "city", color: "#00f0ff", size: 0.4, description: "Amapiano capital, Soweto sound system heritage, and Mzansi deep house.", connections: ["subg_amapiano", "city_london"] },
  { id: "ven_conne_island", name: "Conne Island Leipzig", category: "venue", color: "#eab308", size: 0.28, description: "Historic Connewitz underground bastion for dubstep, punk, and bass culture.", connections: ["city_berlin"] },
  { id: "cur_cercle_colosseum", name: "Cercle Colosseum Live", category: "festival", color: "#fb7185", size: 0.32, bpm: 126, genre: "Melodic Techno", description: "Sensory architectural livestream with Stephan Bodzin at the Roman Colosseum.", connections: ["art_stephanbodzin"] },
  { id: "gear_space_echo", name: "Roland Space Echo RE-201", category: "gear", color: "#84cc16", size: 0.28, description: "Vintage 1974 analog magnetic tape loop delay unit defining Dub Techno and Nils Frahm.", connections: ["art_nilsfrahm", "city_berlin"] },
  { id: "gear_moog_sub37", name: "Moog Subsequent 37", category: "gear", color: "#84cc16", size: 0.28, description: "Analog paraphonic synthesizer delivering signature fat multi-drive sub bass.", connections: ["art_stephanbodzin"] },
  { id: "ven_potsdam_fabrik", name: "Fabrik Potsdam Soundstage", category: "venue", color: "#eab308", size: 0.28, description: "Industrial arts factory and acoustic live hall on the outskirts of Berlin.", connections: ["city_berlin"] },
  { id: "art_ar_rahman", name: "A.R. Rahman (Panchathan)", category: "artist", color: "#c084fc", size: 0.34, bpm: 110, genre: "Soundtrack", description: "Academy Award maestro pioneering eastern-western cinematic synthesis.", connections: ["std_yrf_mumbai", "city_london"] },
];

export const NetworkGraph3D: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const dispatch = useAppDispatch();

  // Dynamic Graph State
  const [nodes, setNodes] = useState<Graph3DNode[]>(INITIAL_GRAPH_NODES);
  const [selectedNode, setSelectedNode] = useState<Graph3DNode | null>(INITIAL_GRAPH_NODES[0]);
  const [hoveredNode, setHoveredNode] = useState<Graph3DNode | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [activePreset, setActivePreset] = useState<string>("overview");
  const [isAutoRotate, setIsAutoRotate] = useState(true);

  // Live Real-Time Expansion State
  const [isExpandingLive, setIsExpandingLive] = useState(true);
  const [expansionSpeed, setExpansionSpeed] = useState<number>(1);
  const [liveEpoch, setLiveEpoch] = useState<number>(428);
  const [edgeCount, setEdgeCount] = useState<number>(24007);
  const [recentSpawnToast, setRecentSpawnToast] = useState<string | null>("Autonomous Expansion Engine Online");

  // Three.js References
  const sceneRef = useRef<THREE.Scene | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const targetCamPos = useRef<THREE.Vector3>(new THREE.Vector3(0, 4, 14));
  const targetLookAt = useRef<THREE.Vector3>(new THREE.Vector3(0, 0, 0));
  const nodeMeshGroupRef = useRef<THREE.Group | null>(null);
  const edgeLineGroupRef = useRef<THREE.Group | null>(null);
  const wavePulsarGroupRef = useRef<THREE.Group | null>(null);

  const flyCameraTo = (camPos: THREE.Vector3, lookPos: THREE.Vector3) => {
    targetCamPos.current.copy(camPos);
    targetLookAt.current.copy(lookPos);
  };

  const handlePresetSelect = (presetId: string) => {
    setActivePreset(presetId);
    if (presetId === "overview") {
      flyCameraTo(new THREE.Vector3(0, 4, 14), new THREE.Vector3(0, 0, 0));
    } else if (presetId === "berlin") {
      flyCameraTo(new THREE.Vector3(-4.0, 1.5, 5.0), new THREE.Vector3(-4.0, 0.5, 0.0));
      setSelectedNode(nodes.find((n) => n.id === "city_berlin") || nodes[0]);
    } else if (presetId === "india") {
      flyCameraTo(new THREE.Vector3(3.8, 0.2, 9.0), new THREE.Vector3(3.5, 0.0, 4.0));
      setSelectedNode(nodes.find((n) => n.id === "city_mumbai") || nodes[0]);
    } else if (presetId === "americas") {
      flyCameraTo(new THREE.Vector3(4.0, -2.0, 6.5), new THREE.Vector3(3.0, -2.0, 2.0));
      setSelectedNode(nodes.find((n) => n.id === "city_la") || nodes[0]);
    } else if (presetId === "asia_africa") {
      flyCameraTo(new THREE.Vector3(2.5, 2.0, -5.0), new THREE.Vector3(3.0, 0.0, -2.0));
      setSelectedNode(nodes.find((n) => n.id === "city_tokyo") || nodes[0]);
    }
  };

  // Trigger Dynamic Node Spawn in Three.js Scene
  const spawnDynamicNode = useCallback(() => {
    setNodes((prevNodes) => {
      // Find a node from pool that isn't spawned yet
      const unspawned = DYNAMIC_EXPANSION_POOL.filter(
        (cand) => !prevNodes.some((existing) => existing.id === cand.id)
      );

      let nodeToSpawn: Graph3DNode;
      if (unspawned.length > 0) {
        const item = unspawned[0];
        // Calculate dynamic position around parent hub
        const parentId = item.connections[0] || "city_berlin";
        const parent = prevNodes.find((n) => n.id === parentId) || prevNodes[0];
        const angle = Math.random() * Math.PI * 2;
        const radius = 1.8 + Math.random() * 1.5;
        const offsetZ = (Math.random() - 0.5) * 2.0;

        nodeToSpawn = {
          ...item,
          position: [
            parent.position[0] + Math.cos(angle) * radius,
            parent.position[1] + Math.sin(angle) * radius,
            parent.position[2] + offsetZ,
          ],
          epochSpawned: liveEpoch,
        };
      } else {
        // Procedurally generate new micro-hub if pool exhausted
        const randId = `dyn_micro_hub_${Date.now().toString().slice(-4)}`;
        const parent = prevNodes[Math.floor(Math.random() * prevNodes.length)];
        const angle = Math.random() * Math.PI * 2;
        const radius = 2.0 + Math.random() * 1.8;

        nodeToSpawn = {
          id: randId,
          name: `Recursive Micro-Hub #${randId.slice(-4)}`,
          category: "venue",
          color: "#eab308",
          size: 0.26,
          position: [
            parent.position[0] + Math.cos(angle) * radius,
            parent.position[1] + Math.sin(angle) * radius,
            parent.position[2] + (Math.random() - 0.5) * 2.2,
          ],
          description: `Autonomous satellite sub-hub spawned via recursive multi-hop wave propagation from ${parent.name}.`,
          connections: [parent.id],
          epochSpawned: liveEpoch,
        };
      }

      setLiveEpoch((prev) => prev + 1);
      setEdgeCount((prev) => prev + Math.floor(25 + Math.random() * 30));
      setRecentSpawnToast(`+ Node Spawned: ${nodeToSpawn.name} (${nodeToSpawn.category.toUpperCase()})`);

      // Add Shockwave Pulsar in Three.js
      if (wavePulsarGroupRef.current) {
        const ringGeo = new THREE.RingGeometry(0.1, 0.3, 32);
        const ringMat = new THREE.MeshBasicMaterial({
          color: new THREE.Color(nodeToSpawn.color),
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 1.0,
          blending: THREE.AdditiveBlending,
        });
        const waveMesh = new THREE.Mesh(ringGeo, ringMat);
        waveMesh.position.set(...nodeToSpawn.position);
        waveMesh.userData = { age: 0, maxAge: 90 };
        wavePulsarGroupRef.current.add(waveMesh);
      }

      return [...prevNodes, nodeToSpawn];
    });
  }, [liveEpoch]);

  // Live Auto-Expansion Interval Loop
  useEffect(() => {
    if (!isExpandingLive) return;
    const intervalMs = Math.max(800, 3000 / expansionSpeed);
    const timer = setInterval(() => {
      spawnDynamicNode();
    }, intervalMs);

    return () => clearInterval(timer);
  }, [isExpandingLive, expansionSpeed, spawnDynamicNode]);

  // Initialize Three.js WebGL Scene
  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;

    // 1. Scene & Fog Setup
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x050508, 0.032);
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(
      55,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 4, 14);
    cameraRef.current = camera;

    // 2. WebGL Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;
    renderer.domElement.style.touchAction = "none";
    renderer.domElement.style.outline = "none";
    container.innerHTML = "";
    container.appendChild(renderer.domElement);

    // 3. OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.rotateSpeed = 0.9;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 0.8;
    controls.maxDistance = 45;
    controls.minDistance = 1.5;
    controls.autoRotate = isAutoRotate;
    controls.autoRotateSpeed = 0.4;
    controlsRef.current = controls;

    // 4. Background Cosmic Starfield (2,000 Particles)
    const starGeo = new THREE.BufferGeometry();
    const starCount = 2000;
    const starPositions = new Float32Array(starCount * 3);
    const starColors = new Float32Array(starCount * 3);

    for (let i = 0; i < starCount; i++) {
      starPositions[i * 3] = (Math.random() - 0.5) * 80;
      starPositions[i * 3 + 1] = (Math.random() - 0.5) * 80;
      starPositions[i * 3 + 2] = (Math.random() - 0.5) * 80;

      const c = new THREE.Color().setHSL(0.55 + Math.random() * 0.15, 0.7, 0.6);
      starColors[i * 3] = c.r;
      starColors[i * 3 + 1] = c.g;
      starColors[i * 3 + 2] = c.b;
    }
    starGeo.setAttribute("position", new THREE.BufferAttribute(starPositions, 3));
    starGeo.setAttribute("color", new THREE.BufferAttribute(starColors, 3));

    const starMat = new THREE.PointsMaterial({
      size: 0.14,
      vertexColors: true,
      transparent: true,
      opacity: 0.7,
      blending: THREE.AdditiveBlending,
    });
    const starField = new THREE.Points(starGeo, starMat);
    scene.add(starField);

    // 5. Lights
    scene.add(new THREE.AmbientLight(0xffffff, 0.8));
    const pLight1 = new THREE.PointLight(0x1db954, 2.5, 40);
    pLight1.position.set(0, 8, 8);
    scene.add(pLight1);

    const pLight2 = new THREE.PointLight(0x00f0ff, 2.2, 40);
    pLight2.position.set(-8, -6, -8);
    scene.add(pLight2);

    // 6. Scene Groups
    const nodeGroup = new THREE.Group();
    const edgeGroup = new THREE.Group();
    const waveGroup = new THREE.Group();
    scene.add(edgeGroup);
    scene.add(nodeGroup);
    scene.add(waveGroup);

    nodeMeshGroupRef.current = nodeGroup;
    edgeLineGroupRef.current = edgeGroup;
    wavePulsarGroupRef.current = waveGroup;

    // 7. Raycasting & Mouse Hover Interactions
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const onPointerMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(nodeGroup.children);

      if (intersects.length > 0) {
        const hit = intersects[0].object as THREE.Mesh;
        if (hit.userData && hit.userData.id) {
          setHoveredNode(hit.userData as Graph3DNode);
          container.style.cursor = "pointer";
          return;
        }
      }
      setHoveredNode(null);
      container.style.cursor = "grab";
    };

    const onClick = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(nodeGroup.children);

      if (intersects.length > 0) {
        const hit = intersects[0].object as THREE.Mesh;
        if (hit.userData && hit.userData.id) {
          setSelectedNode(hit.userData as Graph3DNode);
          const pos = hit.position;
          flyCameraTo(
            new THREE.Vector3(pos.x + 2.5, pos.y + 1.5, pos.z + 4.5),
            pos
          );
        }
      }
    };

    container.addEventListener("pointermove", onPointerMove);
    container.addEventListener("click", onClick);

    // 8. Animation & Render Loop
    let animId: number;
    const clock = new THREE.Clock();

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const delta = clock.getDelta();
      const elapsed = clock.getElapsedTime();

      // Camera Smooth Lerp
      camera.position.lerp(targetCamPos.current, 0.05);
      controls.target.lerp(targetLookAt.current, 0.05);
      controls.update();

      // Rotate Starfield
      starField.rotation.y = elapsed * 0.02;

      // Animate Node Halos & Breathing Scales
      nodeGroup.children.forEach((child, idx) => {
        const mesh = child as THREE.Mesh;
        const waveScale = 1.0 + Math.sin(elapsed * 2.5 + idx * 0.4) * 0.08;
        mesh.scale.set(waveScale, waveScale, waveScale);
      });

      // Animate Expanding Shockwaves
      waveGroup.children.forEach((child) => {
        const ring = child as THREE.Mesh;
        if (ring.userData) {
          ring.userData.age += 1;
          const progress = ring.userData.age / ring.userData.maxAge;
          const scale = 1.0 + progress * 6.0;
          ring.scale.set(scale, scale, scale);
          (ring.material as THREE.MeshBasicMaterial).opacity = Math.max(0, 1.0 - progress);

          if (ring.userData.age >= ring.userData.maxAge) {
            waveGroup.remove(ring);
          }
        }
      });

      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      if (!container) return;
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    };
    window.addEventListener("resize", handleResize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", handleResize);
      container.removeEventListener("pointermove", onPointerMove);
      container.removeEventListener("click", onClick);
      renderer.dispose();
    };
  }, []);

  // Update Three.js Node & Edge Meshes when Nodes State Changes
  useEffect(() => {
    if (!nodeMeshGroupRef.current || !edgeLineGroupRef.current) return;
    const nodeGroup = nodeMeshGroupRef.current;
    const edgeGroup = edgeLineGroupRef.current;

    // Clear previous geometries
    while (nodeGroup.children.length > 0) {
      nodeGroup.remove(nodeGroup.children[0]);
    }
    while (edgeGroup.children.length > 0) {
      edgeGroup.remove(edgeGroup.children[0]);
    }

    const nodePositionMap = new Map<string, THREE.Vector3>();

    // 1. Build Node Meshes
    nodes.forEach((n) => {
      const pos = new THREE.Vector3(...n.position);
      nodePositionMap.set(n.id, pos);

      const geo = new THREE.SphereGeometry(n.size, 32, 32);
      const mat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(n.color),
        emissive: new THREE.Color(n.color),
        emissiveIntensity: 0.6,
        roughness: 0.15,
        metalness: 0.85,
      });

      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.copy(pos);
      mesh.userData = n;
      nodeGroup.add(mesh);

      // Glowing Halo Ring
      const ringGeo = new THREE.RingGeometry(n.size * 1.3, n.size * 1.55, 32);
      const ringMat = new THREE.MeshBasicMaterial({
        color: new THREE.Color(n.color),
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.45,
        blending: THREE.AdditiveBlending,
      });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.position.copy(pos);
      nodeGroup.add(ring);
    });

    // 2. Build Glowing Edge Lines
    const edgeMat = new THREE.LineBasicMaterial({
      color: 0x1db954,
      transparent: true,
      opacity: 0.35,
      blending: THREE.AdditiveBlending,
    });

    const edgePoints: THREE.Vector3[] = [];
    const drawnEdges = new Set<string>();

    nodes.forEach((u) => {
      const uPos = nodePositionMap.get(u.id);
      if (!uPos) return;

      u.connections.forEach((vId) => {
        const vPos = nodePositionMap.get(vId);
        if (!vPos) return;

        const edgeKey = [u.id, vId].sort().join("---");
        if (!drawnEdges.has(edgeKey)) {
          drawnEdges.add(edgeKey);
          edgePoints.push(uPos, vPos);
        }
      });
    });

    if (edgePoints.length > 0) {
      const edgeGeo = new THREE.BufferGeometry().setFromPoints(edgePoints);
      const edgeMesh = new THREE.LineSegments(edgeGeo, edgeMat);
      edgeGroup.add(edgeMesh);
    }
  }, [nodes]);

  return (
    <div
      className={`relative w-full rounded-2xl overflow-hidden border border-white/10 bg-[#050508] transition-all ${
        isFullscreen
          ? "fixed inset-0 z-50 rounded-none h-screen"
          : "h-[560px] sm:h-[620px] shadow-2xl"
      }`}
    >
      {/* 3D WebGL Canvas Mounting Point */}
      <div
        ref={containerRef}
        className="w-full h-full cursor-grab active:cursor-grabbing"
      />

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
              {isExpandingLive ? "AUTONOMOUS EXPANSION LIVE" : "EXPANSION PAUSED"}
            </span>
            <span className="text-white/40 mx-2">•</span>
            <span className="font-bold">EPOCH #{liveEpoch}</span>
            <span className="text-white/40 mx-2">•</span>
            <span>{nodes.length} NODES</span>
            <span className="text-white/40 mx-2">•</span>
            <span>{edgeCount.toLocaleString()} EDGES</span>
          </div>
        </div>

        {/* Live Expansion Controls & Camera Presets */}
        <div className="flex items-center gap-2 pointer-events-auto">
          {/* Preset Buttons */}
          <div className="hidden sm:flex bg-black/85 backdrop-blur-md p-1 rounded-full border border-white/10 text-[11px] font-mono shadow-2xl">
            {[
              { id: "overview", label: "Galaxy" },
              { id: "berlin", label: "Berlin" },
              { id: "india", label: "India (Mumbai/Goa)" },
              { id: "americas", label: "Americas" },
              { id: "asia_africa", label: "Asia/Africa" },
            ].map((preset) => (
              <button
                key={preset.id}
                onClick={() => handlePresetSelect(preset.id)}
                className={`px-3 py-1 rounded-full transition-all ${
                  activePreset === preset.id
                    ? "bg-[#1DB954] text-black font-extrabold shadow-md shadow-[#1DB954]/20"
                    : "text-white/70 hover:text-white"
                }`}
              >
                {preset.label}
              </button>
            ))}
          </div>

          {/* Trigger Immediate Wave Button */}
          <button
            onClick={spawnDynamicNode}
            className="px-3 py-1.5 rounded-full text-xs font-mono font-bold bg-[#1DB954]/20 hover:bg-[#1DB954]/30 border border-[#1DB954]/50 text-[#1DB954] transition-all flex items-center gap-1.5 shadow-xl backdrop-blur-md"
            title="Immediately pulse and spawn new nodes into Three.js"
          >
            <PlusCircle className="w-3.5 h-3.5" />
            <span>+ Pulse Node</span>
          </button>

          {/* Pause / Resume Live Stream */}
          <button
            onClick={() => setIsExpandingLive(!isExpandingLive)}
            className={`px-3 py-1.5 rounded-full text-xs font-mono font-bold border transition-all flex items-center gap-1.5 bg-black/85 backdrop-blur-md ${
              isExpandingLive
                ? "border-[#1DB954] text-[#1DB954]"
                : "border-amber-400 text-amber-400"
            }`}
          >
            {isExpandingLive ? (
              <>
                <Pause className="w-3.5 h-3.5" /> Paused
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-amber-400" /> Resume
              </>
            )}
          </button>

          {/* Auto-Rotate Toggle */}
          <button
            onClick={() => setIsAutoRotate(!isAutoRotate)}
            className={`px-3 py-1.5 rounded-full text-xs font-mono font-bold border transition-all flex items-center gap-1.5 bg-black/85 backdrop-blur-md ${
              isAutoRotate
                ? "border-[#1DB954] text-[#1DB954]"
                : "border-white/10 text-white/50"
            }`}
          >
            <RotateCw className={`w-3.5 h-3.5 ${isAutoRotate ? "animate-spin" : ""}`} style={{ animationDuration: "8s" }} />
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
          <span
            className="w-2.5 h-2.5 rounded-full"
            style={{ backgroundColor: hoveredNode.color }}
          ></span>
          <span className="font-bold">{hoveredNode.name}</span>
          <span className="text-white/40 uppercase text-[10px]">
            ({hoveredNode.category})
          </span>
        </div>
      )}

      {/* Bottom Floating Inspector HUD */}
      {selectedNode && (
        <div className="absolute bottom-4 left-4 right-4 sm:right-auto sm:max-w-md bg-[#121212]/95 backdrop-blur-xl border border-white/10 p-5 rounded-2xl shadow-2xl space-y-3 animate-in fade-in slide-in-from-bottom-4 duration-300">
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
            <div className="p-2.5 bg-black/60 rounded-xl border border-white/5 text-[11px] font-mono text-white/80">
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
