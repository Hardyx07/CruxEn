"use client"
import PromptEnhancer from "@/components/prompt-enhancer"
import PageLoader from "@/components/ui/page-loader"
import { ShootingStars } from "@/components/ui/shooting-stars"
import { StarsBackground } from "@/components/ui/stars-background"

export default function Home() {
  return (
    <PageLoader>
      <main className="min-h-screen relative overflow-hidden bg-background/80 text-foreground selection:bg-primary/30">
        {/* Stars Background Layer */}
        <div className="fixed inset-0 z-0">
          <StarsBackground 
            starDensity={0.0002}
            allStarsTwinkle={true}
            twinkleProbability={0.8}
            minTwinkleSpeed={0.5}
            maxTwinkleSpeed={1.2}
          />
          <ShootingStars 
            minSpeed={15}
            maxSpeed={35}
            minDelay={800}
            maxDelay={3000}
            starColor="#3A7BFF"
            trailColor="#4A4AFF"
            starWidth={12}
            starHeight={2}
          />
        </div>

        {/* Floating orbs for depth - Starry Theme */}
        <div className="fixed inset-0 pointer-events-none overflow-hidden z-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-primary/10 rounded-full blur-[100px] animate-float-slow mix-blend-screen" />
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-900/15 rounded-full blur-[120px] animate-float-slow-delayed mix-blend-screen" />
          <div className="absolute top-1/2 left-1/3 w-64 h-64 bg-blue-900/10 rounded-full blur-[80px] animate-float-medium mix-blend-screen" />
          <div className="absolute top-1/3 right-1/4 w-80 h-80 bg-indigo-900/15 rounded-full blur-[90px] animate-float-slow mix-blend-screen" style={{ animationDelay: '5s' }} />
          <div className="absolute top-3/4 left-1/2 w-56 h-56 bg-accent/8 rounded-full blur-[70px] animate-float-medium mix-blend-screen" style={{ animationDelay: '2s' }} />
        </div>

        <PromptEnhancer />
      </main>
    </PageLoader>
  )
}
