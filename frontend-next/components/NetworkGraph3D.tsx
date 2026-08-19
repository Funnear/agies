"use client";

import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";

interface NodeData {
  id: string;
  name: string;
  type: "city" | "studio" | "label" | "artist" | "venue";
  position: THREE.Vector3;
  color: string;
  size: number;
}

export const NetworkGraph3D: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [selectedNode, setSelectedNode] = useState<NodeData | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      60,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 5, 12);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Nodes Catalog
    const nodes: NodeData[] = [
      { id: "berlin", name: "Berlin Hub", type: "city", position: new THREE.Vector3(-3.5, 0, 0), color: "#00f0ff", size: 0.35 },
      { id: "london", name: "London Hub", type: "city", position: new THREE.Vector3(0, 1.5, -2), color: "#00f0ff", size: 0.35 },
      { id: "la", name: "Los Angeles Hub", type: "city", position: new THREE.Vector3(4, -1, 1), color: "#00f0ff", size: 0.35 },
      { id: "stockholm", name: "Stockholm Hub", type: "city", position: new THREE.Vector3(1, 3, 0), color: "#00f0ff", size: 0.3 },
      { id: "paris", name: "Paris Hub", type: "city", position: new THREE.Vector3(-1.5, -1.5, -1), color: "#00f0ff", size: 0.3 },
      { id: "hansa", name: "Hansa Tonstudio", type: "studio", position: new THREE.Vector3(-4.2, 1, 0.5), color: "#a855f7", size: 0.25 },
      { id: "abbey", name: "Abbey Road Studios", type: "studio", position: new THREE.Vector3(-0.5, 2.5, -2.5), color: "#a855f7", size: 0.25 },
      { id: "funkhaus", name: "Funkhaus Berlin", type: "studio", position: new THREE.Vector3(-3, -1.2, 0.8), color: "#a855f7", size: 0.25 },
      { id: "ostgut", name: "Ostgut Ton", type: "label", position: new THREE.Vector3(-2.8, 1.8, 0.2), color: "#f59e0b", size: 0.22 },
      { id: "warp", name: "Warp Records", type: "label", position: new THREE.Vector3(0.8, 0.5, -3), color: "#f59e0b", size: 0.22 },
      { id: "bodzin", name: "Stephan Bodzin", type: "artist", position: new THREE.Vector3(-4.8, -0.5, 1.2), color: "#10b981", size: 0.2 },
      { id: "aphex", name: "Aphex Twin", type: "artist", position: new THREE.Vector3(1.5, -0.8, -3.2), color: "#10b981", size: 0.2 },
      { id: "berghain", name: "Berghain / Panorama Bar", type: "venue", position: new THREE.Vector3(-2.2, 0.5, 1.5), color: "#ec4899", size: 0.26 },
      { id: "fabric", name: "Fabric London", type: "venue", position: new THREE.Vector3(-0.8, 0.8, -1.2), color: "#ec4899", size: 0.26 },
    ];

    const nodeMeshes: { mesh: THREE.Mesh; data: NodeData }[] = [];

    // Create 3D Nodes
    nodes.forEach((n) => {
      const geo = new THREE.SphereGeometry(n.size, 24, 24);
      const mat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(n.color),
        emissive: new THREE.Color(n.color),
        emissiveIntensity: 0.5,
        roughness: 0.2,
        metalness: 0.8,
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.copy(n.position);
      scene.add(mesh);
      nodeMeshes.push({ mesh, data: n });

      // Add Halo Ring
      const ringGeo = new THREE.RingGeometry(n.size * 1.3, n.size * 1.5, 32);
      const ringMat = new THREE.MeshBasicMaterial({
        color: new THREE.Color(n.color),
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.4,
      });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.position.copy(n.position);
      ring.rotation.x = Math.PI / 2;
      scene.add(ring);
    });

    // Edges & Corridors
    const edgePairs = [
      ["berlin", "london", "#00f0ff", 2], // European Club Highway
      ["stockholm", "la", "#ec4899", 2.5], // Transatlantic Pop Axis
      ["london", "la", "#00f0ff", 1.5],
      ["paris", "london", "#00f0ff", 1.5],
      ["berlin", "hansa", "#a855f7", 1],
      ["berlin", "funkhaus", "#a855f7", 1],
      ["london", "abbey", "#a855f7", 1],
      ["berlin", "ostgut", "#f59e0b", 1],
      ["london", "warp", "#f59e0b", 1],
      ["ostgut", "bodzin", "#10b981", 1],
      ["warp", "aphex", "#10b981", 1],
      ["berlin", "berghain", "#ec4899", 1],
      ["london", "fabric", "#ec4899", 1],
      ["bodzin", "aphex", "#10b981", 1], // Acoustic similarity
    ];

    edgePairs.forEach(([sourceId, targetId, colorStr]) => {
      const s = nodes.find((n) => n.id === sourceId);
      const t = nodes.find((n) => n.id === targetId);
      if (s && t) {
        const lineGeo = new THREE.BufferGeometry().setFromPoints([
          s.position,
          t.position,
        ]);
        const lineMat = new THREE.LineBasicMaterial({
          color: new THREE.Color(colorStr),
          transparent: true,
          opacity: 0.6,
          linewidth: 2,
        });
        const line = new THREE.Line(lineGeo, lineMat);
        scene.add(line);
      }
    });

    // Lighting
    const light1 = new THREE.PointLight(0x00f0ff, 3, 50);
    light1.position.set(5, 8, 10);
    scene.add(light1);

    const light2 = new THREE.PointLight(0xa855f7, 2, 50);
    light2.position.set(-5, -5, 5);
    scene.add(light2);

    scene.add(new THREE.AmbientLight(0x0a1128));

    // Animation & Rotation
    let animId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const elapsed = clock.getElapsedTime();

      scene.rotation.y = elapsed * 0.04;
      scene.rotation.x = Math.sin(elapsed * 0.03) * 0.05;

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
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animId);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="w-full h-[520px] rounded-xl overflow-hidden relative border border-cyan-500/20 bg-slate-950/90 shadow-2xl backdrop-blur-md"
    >
      <div className="absolute top-4 left-4 z-10 flex gap-2 flex-wrap">
        <span className="px-3 py-1 bg-cyan-500/10 border border-cyan-500/30 rounded-full text-xs font-mono text-cyan-400">
          507 ENTITY NODES
        </span>
        <span className="px-3 py-1 bg-purple-500/10 border border-purple-500/30 rounded-full text-xs font-mono text-purple-400">
          1,432 RELATIONS
        </span>
        <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 rounded-full text-xs font-mono text-emerald-400">
          12 INTER-CITY CORRIDORS
        </span>
      </div>

      <div className="absolute bottom-4 left-4 z-10 bg-slate-900/90 border border-slate-800 p-3 rounded-lg backdrop-blur-md max-w-sm text-xs text-slate-300 font-mono">
        <div className="font-bold text-cyan-400 mb-1">
          🌌 THREE.JS 3D KNOWLEDGE UNIVERSE
        </div>
        <div>Rotate & Explore Global Studios, Labels, Venues, and Trade Axes</div>
      </div>
    </div>
  );
};
