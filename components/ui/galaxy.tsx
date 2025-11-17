"use client"

import React, { useEffect, useRef } from "react"

interface GalaxyProps {
  className?: string
}

export function Galaxy({ className = "" }: GalaxyProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    // Set canvas size
    const setCanvasSize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    setCanvasSize()
    window.addEventListener("resize", setCanvasSize)

    // Create stars
    const stars: Array<{
      x: number
      y: number
      radius: number
      opacity: number
      vx: number
      vy: number
    }> = []
    const starCount = 200

    for (let i = 0; i < starCount; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 1.5,
        opacity: Math.random() * 0.5 + 0.5,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
      })
    }

    // Animation loop
    const animate = () => {
      // Clear with gradient background
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height)
      gradient.addColorStop(0, "#232323")
      gradient.addColorStop(0.5, "#0c1821")
      gradient.addColorStop(1, "#0c1821")
      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Draw and update stars
      stars.forEach((star) => {
        // Update position
        star.x += star.vx
        star.y += star.vy

        // Wrap around edges
        if (star.x < 0) star.x = canvas.width
        if (star.x > canvas.width) star.x = 0
        if (star.y < 0) star.y = canvas.height
        if (star.y > canvas.height) star.y = 0

        // Draw star with glow
        ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`
        ctx.beginPath()
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2)
        ctx.fill()

        // Draw glow
        ctx.strokeStyle = `rgba(200, 150, 255, ${star.opacity * 0.3})`
        ctx.lineWidth = star.radius * 2
        ctx.beginPath()
        ctx.arc(star.x, star.y, star.radius * 1.5, 0, Math.PI * 2)
        ctx.stroke()
      })

      // Draw nebula-like clusters
      ctx.fillStyle = "rgba(100, 50, 200, 0.05)"
      for (let i = 0; i < 3; i++) {
        const x = (canvas.width / 3) * i + (Math.sin(Date.now() * 0.0001) * 50)
        const y = (canvas.height / 3) * i + (Math.cos(Date.now() * 0.0001) * 50)
        const gradient2 = ctx.createRadialGradient(x, y, 0, x, y, 400)
        gradient2.addColorStop(0, "rgba(150, 100, 255, 0.2)")
        gradient2.addColorStop(1, "rgba(150, 100, 255, 0)")
        ctx.fillStyle = gradient2
        ctx.fillRect(x - 400, y - 400, 800, 800)
      }

      requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener("resize", setCanvasSize)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className={`fixed inset-0 -z-10 ${className}`}
    />
  )
}
