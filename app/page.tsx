"use client"
import PromptEnhancer from "@/components/prompt-enhancer"
import Hyperspeed from "@/components/Hyperspeed"
import PageLoader from "@/components/page-loader"

export default function Home() {
  return (
    <PageLoader>
      <main className="min-h-screen relative overflow-hidden bg-background/80 text-foreground selection:bg-primary/30">
        <div className="fixed inset-0 z-0">
          <Hyperspeed />
        </div>

        {/* Floating orbs for depth - Hyperspeed Theme */}
        <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
          <div className="absolute top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-[100px] animate-float-slow mix-blend-screen" />
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-900/20 rounded-full blur-[120px] animate-float-slow-delayed mix-blend-screen" />
          <div className="absolute top-1/2 left-1/3 w-64 h-64 bg-blue-900/20 rounded-full blur-[80px] animate-float-medium mix-blend-screen" />
          <div className="absolute top-1/3 right-1/4 w-80 h-80 bg-indigo-900/20 rounded-full blur-[90px] animate-float-slow mix-blend-screen" style={{ animationDelay: '5s' }} />
        </div>

        <PromptEnhancer />
      </main>
    </PageLoader>
  )
}
