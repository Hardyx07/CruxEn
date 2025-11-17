"use client"
import PromptEnhancer from "@/components/prompt-enhancer"
import { Galaxy } from "@/components/ui/galaxy"

export default function Home() {
  return (
    <main className="min-h-screen relative overflow-hidden">
      <Galaxy />
      
      {/* Floating orbs for depth - Monochrome theme */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-20 left-10 w-72 h-72 bg-white/3 rounded-full blur-3xl animate-float-slow" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-white/4 rounded-full blur-3xl animate-float-slow-delayed" />
        <div className="absolute top-1/2 left-1/3 w-64 h-64 bg-white/2 rounded-full blur-3xl animate-float-medium" />
        <div className="absolute top-1/3 right-1/4 w-80 h-80 bg-white/3 rounded-full blur-3xl animate-float-slow" style={{ animationDelay: '5s' }} />
      </div>

      <PromptEnhancer />
    </main>
  )
}
