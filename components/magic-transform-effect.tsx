"use client"

import { useEffect, useState } from "react"

export default function MagicTransformEffect() {
  const [particles, setParticles] = useState<
    Array<{ id: number; left: string; top: string; delay: string; duration: string }>
  >([])

  useEffect(() => {
    const newParticles = Array.from({ length: 20 }, (_, i) => ({
      id: i,
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      delay: `${Math.random() * 0.4}s`,
      duration: `${1.2 + Math.random() * 0.6}s`,
    }))
    setParticles(newParticles)
  }, [])

  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-lg">
      {/* Main shimmer wave effect */}
      <div className="absolute inset-0 shimmer-wave rounded-lg" />

      {/* Radiating glow expand effect */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div
          className="glow-expand w-32 h-32 bg-gradient-to-r from-accent to-accent/50 rounded-full"
          style={{
            filter: "blur(30px)",
          }}
        />
      </div>

      {/* Particle effects with varied durations */}
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="absolute float-up w-2.5 h-2.5 bg-gradient-to-r from-accent to-accent/50 rounded-full"
          style={{
            left: particle.left,
            top: particle.top,
            animationDelay: particle.delay,
            animationDuration: particle.duration,
          }}
        />
      ))}

      {/* Center pulsing core */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="w-16 h-16 rounded-full border-2 border-accent/40 pulse-soft" />
      </div>
    </div>
  )
}
