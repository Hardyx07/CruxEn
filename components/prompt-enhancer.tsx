"use client"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import FrameworkSelector from "./framework-selector"
import PromptInput from "./prompt-input"
import MagicTransformEffect from "./magic-transform-effect"

type Framework = "coding" | "research" | "study" | "business"

export default function PromptEnhancer() {
  const [rawPrompt, setRawPrompt] = useState("")
  const [enhancedPrompt, setEnhancedPrompt] = useState("")
  const [framework, setFramework] = useState<Framework>("coding")
  const [isLoading, setIsLoading] = useState(false)
  const [showTransform, setShowTransform] = useState(false)
  const promptBoxRef = useRef<HTMLDivElement>(null)

  const handleEnhance = async () => {
    if (!rawPrompt.trim()) return

    setIsLoading(true)
    setShowTransform(true)

    try {
      const response = await fetch("/api/enhance-prompt", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: rawPrompt,
          framework,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to enhance prompt")
      }

      const data = await response.json()

      setTimeout(() => {
        setEnhancedPrompt(data.enhanced)
        setRawPrompt("")
        setShowTransform(false)
      }, 1600)
    } catch (error) {
      console.error("Error enhancing prompt:", error)
      setShowTransform(false)
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 py-16">
      <div className="mb-16 text-center max-w-2xl mx-auto slide-in">
        <div className="mb-6 inline-flex items-center gap-2 px-4 py-1.5 bg-accent/10 border border-accent/30 rounded-full">
          <span className="w-2 h-2 bg-accent rounded-full pulse-soft" />
          <span className="text-sm font-medium text-accent">AI-Powered Enhancement</span>
        </div>
        <h1 className="text-5xl md:text-6xl font-bold mb-4 text-foreground tracking-tight">Refine Your Prompts</h1>
        <p className="text-lg text-muted-foreground leading-relaxed">
          Transform raw ideas into precise, context-aware prompts tailored to your specific needs
        </p>
      </div>

      <div className="w-full max-w-2xl space-y-8">
        {/* Framework Selector */}
        <FrameworkSelector framework={framework} onFrameworkChange={setFramework} />

        {/* Main Prompt Box */}
        <div ref={promptBoxRef} className="relative">
          {showTransform && <MagicTransformEffect />}

          <Card className="border border-accent/20 bg-card/40 backdrop-blur-md hover:border-accent/40 hover:bg-card/60 transition-all duration-500 shadow-2xl">
            <div className="p-8 md:p-10">
              {enhancedPrompt ? (
                <div className="space-y-6 fade-in">
                  <div className="flex items-center gap-2 mb-4">
                    <div className="w-3 h-3 rounded-full bg-gradient-to-r from-accent to-accent/60" />
                    <span className="text-sm font-semibold text-accent uppercase tracking-wide">Enhanced Result</span>
                  </div>
                  <p className="text-foreground text-lg leading-relaxed font-light">{enhancedPrompt}</p>
                  <Button
                    onClick={() => {
                      setEnhancedPrompt("")
                      setRawPrompt("")
                    }}
                    className="w-full mt-6 bg-accent/90 hover:bg-accent text-accent-foreground font-semibold py-3 rounded-lg transition-all duration-300"
                  >
                    ✨ Create Another Prompt
                  </Button>
                </div>
              ) : (
                <>
                  <PromptInput
                    value={rawPrompt}
                    onChange={setRawPrompt}
                    placeholder="Share your raw idea or prompt here..."
                  />
                  <Button
                    onClick={handleEnhance}
                    disabled={!rawPrompt.trim() || isLoading}
                    className="w-full mt-8 bg-accent hover:bg-accent/90 disabled:opacity-50 disabled:cursor-not-allowed text-accent-foreground font-semibold py-3 text-base rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl"
                    size="lg"
                  >
                    {isLoading ? (
                      <span className="flex items-center justify-center gap-2">
                        <span className="inline-block w-4 h-4 border-2 border-accent-foreground border-t-transparent rounded-full animate-spin" />
                        Enhancing with AI Magic...
                      </span>
                    ) : (
                      "✨ Enhance with Magic"
                    )}
                  </Button>
                </>
              )}
            </div>
          </Card>
        </div>

        <div className="grid md:grid-cols-4 gap-4 mt-12">
          {[
            { label: "Precise", desc: "Contextually accurate" },
            { label: "Fast", desc: "Real-time processing" },
            { label: "Flexible", desc: "Multiple frameworks" },
            { label: "Smart", desc: "AI-powered" },
          ].map((item) => (
            <div
              key={item.label}
              className="px-5 py-4 rounded-lg bg-card/30 border border-border/40 hover:border-accent/30 hover:bg-card/50 transition-all duration-300 text-center"
            >
              <div className="text-sm font-semibold text-foreground mb-1">{item.label}</div>
              <div className="text-xs text-muted-foreground">{item.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
