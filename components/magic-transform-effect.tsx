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
    <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-3xl z-50">
      {/* Backdrop blur */}
      <div className="absolute inset-0 bg-background/80 backdrop-blur-xl rounded-3xl" />
      
      {/* Main shimmer wave effect */}
      <div className="absolute inset-0 shimmer-wave rounded-3xl" />

      {/* Radiating glow expand effect - Multiple layers */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div
          className="glow-expand w-40 h-40 bg-linear-to-r from-accent via-primary to-accent rounded-full"
          style={{
            filter: "blur(40px)",
          }}
        />
      </div>
      <div className="absolute inset-0 flex items-center justify-center">
        <div
          className="glow-expand w-28 h-28 bg-accent rounded-full"
          style={{
            filter: "blur(25px)",
            animationDelay: "0.2s",
          }}
        />
      </div>

      {/* Particle effects with varied durations */}
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="absolute float-up w-3 h-3 bg-linear-to-br from-accent via-primary/80 to-accent/60 rounded-full shadow-lg shadow-accent/50"
          style={{
            left: particle.left,
            top: particle.top,
            animationDelay: particle.delay,
            animationDuration: particle.duration,
          }}
        />
      ))}

      {/* Center pulsing core with rings */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="relative">
          <div className="w-20 h-20 rounded-full border-2 border-accent/60 pulse-soft" />
          <div className="absolute inset-0 w-20 h-20 rounded-full border-2 border-accent/40 pulse-soft" style={{ animationDelay: "0.5s" }} />
          <div className="absolute inset-0 w-20 h-20 rounded-full border border-accent/20 pulse-soft" style={{ animationDelay: "1s" }} />
          
          {/* Center icon */}
          <div className="absolute inset-0 flex items-center justify-center">
            <svg className="w-8 h-8 text-accent animate-spin" style={{ animationDuration: "2s" }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
        </div>
      </div>

      {/* Loading text */}
      <div className="absolute bottom-8 left-0 right-0 flex justify-center">
        <div className="bg-card/90 backdrop-blur-xl px-6 py-3 rounded-full border border-accent/30 shadow-lg">
          <span className="text-sm font-semibold text-accent flex items-center gap-2">
            <span className="inline-block w-2 h-2 bg-accent rounded-full animate-pulse"></span>
            Enhancing your prompt...
          </span>
        </div>
      </div>
    </div>
  )
}
