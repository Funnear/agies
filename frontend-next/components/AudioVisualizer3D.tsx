"use client";

import React, { useEffect, useRef } from "react";
import * as THREE from "three";

interface AudioVisualizer3DProps {
  bpm?: number;
  genre?: string;
  isPlaying?: boolean;
}

export const AudioVisualizer3D: React.FC<AudioVisualizer3DProps> = ({
  bpm = 132,
  genre = "Techno",
  isPlaying = true,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      60,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    camera.position.z = 4.5;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // 1. Central Wireframe Icosahedron / Torus
    const geometry = new THREE.IcosahedronGeometry(1.6, 3);
    const originalPositions = geometry.attributes.position.clone();

    const material = new THREE.MeshStandardMaterial({
      color: new THREE.Color("#00f0ff"),
      wireframe: true,
      emissive: new THREE.Color("#9d4edd"),
      emissiveIntensity: 0.6,
      roughness: 0.2,
      metalness: 0.8,
    });

    const sphereMesh = new THREE.Mesh(geometry, material);
    scene.add(sphereMesh);

    // 2. Floating Ambient Particle Nebula
    const particleCount = 600;
    const particleGeo = new THREE.BufferGeometry();
    const particlePos = new Float32Array(particleCount * 3);
    const particleColors = new Float32Array(particleCount * 3);

    const cyan = new THREE.Color("#00f0ff");
    const purple = new THREE.Color("#a855f7");
    const green = new THREE.Color("#10b981");

    for (let i = 0; i < particleCount; i++) {
      const radius = 2.5 + Math.random() * 3.5;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);

      particlePos[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      particlePos[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      particlePos[i * 3 + 2] = radius * Math.cos(phi);

      const color = i % 3 === 0 ? cyan : i % 3 === 1 ? purple : green;
      particleColors[i * 3] = color.r;
      particleColors[i * 3 + 1] = color.g;
      particleColors[i * 3 + 2] = color.b;
    }

    particleGeo.setAttribute(
      "position",
      new THREE.BufferAttribute(particlePos, 3)
    );
    particleGeo.setAttribute(
      "color",
      new THREE.BufferAttribute(particleColors, 3)
    );

    const particleMat = new THREE.PointsMaterial({
      size: 0.04,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending,
    });

    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // 3. Lights
    const pointLight = new THREE.PointLight(0x00f0ff, 2.5, 50);
    pointLight.position.set(4, 4, 4);
    scene.add(pointLight);

    const purpleLight = new THREE.PointLight(0xa855f7, 2, 50);
    purpleLight.position.set(-4, -4, 2);
    scene.add(purpleLight);

    const ambientLight = new THREE.AmbientLight(0x111827);
    scene.add(ambientLight);

    // Animation Loop (Audio-reactive pulse based on BPM)
    let animationFrameId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();
      const speed = (bpm / 120.0) * 1.5;

      // Rotate objects
      sphereMesh.rotation.x = elapsedTime * 0.25 * speed;
      sphereMesh.rotation.y = elapsedTime * 0.35 * speed;
      particles.rotation.y = -elapsedTime * 0.08 * speed;

      // Deform sphere vertices according to rhythmic beat pulse
      const positions = geometry.attributes.position;
      const orig = originalPositions;
      const beatPulse = Math.sin(elapsedTime * (bpm / 60) * Math.PI * 2);

      for (let i = 0; i < positions.count; i++) {
        const u = orig.getX(i);
        const v = orig.getY(i);
        const w = orig.getZ(i);

        const noise =
          Math.sin(u * 3.0 + elapsedTime * 4.0) *
          Math.cos(v * 3.0 + elapsedTime * 4.0) *
          0.15;
        const scale = 1.0 + noise + (beatPulse > 0.7 ? 0.08 : 0.0);

        positions.setXYZ(i, u * scale, v * scale, w * scale);
      }
      positions.needsUpdate = true;

      renderer.render(scene, camera);
    };

    animate();

    // Resize Handler
    const handleResize = () => {
      if (!container) return;
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationFrameId);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      geometry.dispose();
      material.dispose();
      particleGeo.dispose();
      particleMat.dispose();
      renderer.dispose();
    };
  }, [bpm, genre, isPlaying]);

  return (
    <div
      ref={containerRef}
      className="w-full h-72 rounded-xl overflow-hidden relative cursor-grab active:cursor-grabbing border border-cyan-500/20 bg-slate-950/80 shadow-2xl backdrop-blur-md"
    >
      <div className="absolute top-3 left-3 px-3 py-1 bg-cyan-500/10 border border-cyan-500/30 rounded-full text-xs font-mono text-cyan-400 backdrop-blur-md z-10 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
        3D MEL-TEMPOGRAM PULSE: {bpm} BPM • {genre.toUpperCase()}
      </div>
      <div className="absolute bottom-3 right-3 text-[10px] font-mono text-slate-400 bg-slate-900/80 px-2 py-1 rounded border border-slate-800">
        Three.js WebGL Audio Engine (arXiv:2110.08862)
      </div>
    </div>
  );
};
