"use client";
import { cn } from "@/lib/utils";
import React, { useEffect, useRef, useState } from "react";

interface Star {
  x: number;
  y: number;
  z: number;
  size: number;
  twinkleOffset: number;
  twinkleSpeed: number;
}

interface StarsBackgroundProps {
  starDensity?: number;
  allStarsTwinkle?: boolean;
  twinkleProbability?: number;
  minTwinkleSpeed?: number;
  maxTwinkleSpeed?: number;
  className?: string;
}

export const StarsBackground: React.FC<StarsBackgroundProps> = ({
  starDensity = 0.00015,
  allStarsTwinkle = true,
  twinkleProbability = 0.7,
  minTwinkleSpeed = 0.5,
  maxTwinkleSpeed = 1,
  className,
}) => {
  const [stars, setStars] = useState<Star[]>([]);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number | null>(null);
  const dimensionsRef = useRef({ width: 0, height: 0 });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const updateCanvasSize = () => {
      const rect = canvas.getBoundingClientRect();
      const { width, height } = rect;
      
      // Only update if size actually changed to prevent unnecessary rerenders
      if (dimensionsRef.current.width !== width || dimensionsRef.current.height !== height) {
        canvas.width = width;
        canvas.height = height;
        dimensionsRef.current = { width, height };
        
        // Generate stars only when canvas size changes
        const numStars = Math.floor(width * height * starDensity);
        const newStars: Star[] = [];
        
        for (let i = 0; i < numStars; i++) {
          newStars.push({
            x: Math.random() * width,
            y: Math.random() * height,
            z: Math.random(),
            size: Math.random() * 1.5 + 0.5,
            twinkleOffset: Math.random() * Math.PI * 2,
            twinkleSpeed: minTwinkleSpeed + Math.random() * (maxTwinkleSpeed - minTwinkleSpeed),
          });
        }
        
        setStars(newStars);
      }
    };

    updateCanvasSize();

    const handleResize = () => {
      updateCanvasSize();
    };

    window.addEventListener("resize", handleResize);
    
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [starDensity, minTwinkleSpeed, maxTwinkleSpeed]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || stars.length === 0) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const animate = (time: number) => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      stars.forEach((star) => {
        let opacity = 0.3 + Math.sin(time * 0.001 * star.twinkleSpeed + star.twinkleOffset) * 0.3;
        
        if (allStarsTwinkle && Math.random() < twinkleProbability) {
          opacity *= 0.6 + Math.sin(time * 0.002 * star.twinkleSpeed + star.twinkleOffset) * 0.4;
        }
        
        // Ensure opacity stays within reasonable bounds
        opacity = Math.max(0.1, Math.min(1, opacity));
        
        ctx.globalAlpha = opacity;
        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
        ctx.fill();
      });
      
      animationRef.current = requestAnimationFrame(animate);
    };

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [stars, allStarsTwinkle, twinkleProbability]);

  return (
    <canvas
      ref={canvasRef}
      className={cn(
        "fixed inset-0 z-0 h-full w-full pointer-events-none",
        className
      )}
    />
  );
};