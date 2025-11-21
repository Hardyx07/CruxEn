"use client"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { LiquidButton } from "@/components/animate-ui/components/buttons/liquid"
import FrameworkSelector from "./framework-selector"
import PromptInput from "./prompt-input"
import MagicTransformEffect from "./magic-transform-effect"
import { optimizePrompt } from "@/lib/api-client"
import ReactMarkdown from 'react-markdown'

export default function PromptEnhancer() {
  const [rawPrompt, setRawPrompt] = useState("")
  const [enhancedPrompt, setEnhancedPrompt] = useState("")
  const [selectedUseCase, setSelectedUseCase] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [showTransform, setShowTransform] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const promptBoxRef = useRef<HTMLDivElement>(null)

  const handleEnhance = async () => {
    if (!rawPrompt.trim() || !selectedUseCase) return

    setIsLoading(true)
    setShowTransform(true)
    setError(null)

    try {
      const response = await optimizePrompt(rawPrompt, selectedUseCase)

      if (response.error) {
        throw new Error(response.error)
      }

      setTimeout(() => {
        setEnhancedPrompt(response.optimized_prompt)
        setRawPrompt("")
        setShowTransform(false)
        setIsLoading(false)
      }, 1600)
    } catch (err) {
      console.error("Error enhancing prompt:", err)
      setError(
        err instanceof Error ? err.message : "Failed to enhance prompt"
      )
      setShowTransform(false)
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 py-16 relative z-10">
      {/* Hero Section with Modern Typography */}
      <div className="mb-20 text-center max-w-5xl mx-auto space-y-8">
        <div className="mb-4">
          <span className="text-xs font-semibold text-muted-foreground tracking-[0.3em] uppercase">Our Commitment</span>
        </div>

        <h1 className="text-6xl md:text-7xl lg:text-[8rem] font-light mb-8 text-foreground tracking-tight leading-[0.95] font-serif">
          We're just making Good Prompts like it's 2025
        </h1>

        <p className="text-lg md:text-xl text-muted-foreground/80 leading-relaxed font-light max-w-2xl mx-auto mt-12">
          Transform raw ideas into precise, context-aware prompts tailored to your specific needs
        </p>
      </div>

      <div className="w-full max-w-4xl space-y-8">
        {/* Framework Selector Card */}
        <div className="relative z-50">
          <div className="relative bg-card/30 backdrop-blur-xl border border-border/50 rounded-2xl p-6 shadow-2xl">
            <FrameworkSelector
              selectedUseCase={selectedUseCase}
              onUseCaseChange={setSelectedUseCase}
            />
          </div>
        </div>

        {/* Main Prompt Box with Enhanced Glassmorphism */}
        <div ref={promptBoxRef} className="relative z-40">
          <Card className="relative border-2 border-accent/30 bg-linear-to-br from-card/40 via-card/30 to-card/20 backdrop-blur-2xl shadow-2xl rounded-3xl overflow-hidden">
            {/* Glass reflection effect */}
            <div className="absolute inset-0 bg-linear-to-br from-white/5 via-transparent to-transparent pointer-events-none"></div>

            <div className="relative p-8 md:p-12">
              {enhancedPrompt ? (
                <div className="space-y-8 fade-in">
                  {/* Result Header with Icon */}
                  <div className="flex items-center gap-3 mb-6 pb-6 border-b border-accent/20">
                    <div className="relative">
                      <div className="relative w-10 h-10 rounded-full bg-linear-to-br from-accent via-accent/80 to-accent/60 flex items-center justify-center shadow-lg shadow-accent/30">
                        <svg className="w-5 h-5 text-accent-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    </div>
                    <div>
                      <div className="text-base font-bold text-accent uppercase tracking-wider">Enhanced Result</div>
                      <div className="text-xs text-muted-foreground">Optimized & Ready to Use</div>
                    </div>
                  </div>

                  {/* Enhanced Prompt Display */}
                  <div className="relative">
                    <div className="absolute -left-4 top-0 bottom-0 w-1 bg-linear-to-b from-accent via-accent/60 to-transparent rounded-full"></div>
                    <div className="text-foreground text-lg md:text-xl leading-relaxed font-light pl-4 prose prose-invert max-w-none">
                      <ReactMarkdown>{enhancedPrompt}</ReactMarkdown>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex gap-3 pt-4">
                    <Button
                      onClick={() => {
                        navigator.clipboard.writeText(enhancedPrompt)
                      }}
                      className="flex-1 bg-secondary/80 hover:bg-secondary text-secondary-foreground font-semibold py-4 rounded-xl"
                    >
                      <span className="flex items-center justify-center gap-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                        Copy
                      </span>
                    </Button>
                    <Button
                      onClick={() => {
                        setEnhancedPrompt("")
                        setRawPrompt("")
                      }}
                      className="flex-1 bg-linear-to-r from-accent via-accent/90 to-accent/80 text-accent-foreground font-bold py-4 rounded-xl shadow-lg"
                    >
                      <span className="flex items-center justify-center gap-2">
                        <span className="text-lg">✨</span>
                        Create Another
                      </span>
                    </Button>
                  </div>
                </div>
              ) : (
                <>
                  <PromptInput
                    value={rawPrompt}
                    onChange={setRawPrompt}
                    placeholder="Share your raw idea or prompt here..."
                  />
                  <LiquidButton
                    onClick={handleEnhance}
                    disabled={!rawPrompt.trim() || !selectedUseCase || isLoading}
                    className="w-full mt-8"
                    variant="default"
                    size="lg"
                  >
                    {isLoading ? (
                      <span className="flex items-center justify-center gap-3">
                        <span className="relative inline-block w-5 h-5">
                          <span className="absolute inset-0 border-3 border-current/30 rounded-full"></span>
                          <span className="absolute inset-0 border-3 border-current border-t-transparent rounded-full animate-spin"></span>
                        </span>
                        <span className="font-bold">Enhancing with AI Magic...</span>
                      </span>
                    ) : (
                      <span className="flex items-center justify-center gap-2">
                        <span className="text-xl">✨</span>
                        <span className="font-bold">Enhance with Magic</span>
                        <span className="text-xl">✨</span>
                      </span>
                    )}
                  </LiquidButton>
                  {error && (
                    <div className="mt-6 p-4 bg-destructive/10 backdrop-blur-xl border border-destructive/30 rounded-xl text-sm text-destructive font-medium shadow-lg flex items-start gap-3">
                      <svg className="w-5 h-5 shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                      <span>{error}</span>
                    </div>
                  )}
                </>
              )}
            </div>
          </Card>
        </div>

        {/* Feature Cards with Modern Design */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-16">
          {[
            { label: "Precise", desc: "Contextually accurate", icon: "🎯" },
            { label: "Fast", desc: "Real-time processing", icon: "⚡" },
            { label: "Flexible", desc: "Multiple frameworks", icon: "🔄" },
            { label: "Smart", desc: "AI-powered", icon: "🧠" },
          ].map((item, index) => (
            <div
              key={item.label}
              className="group relative overflow-hidden"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Gradient glow on hover */}
              <div className="absolute -inset-0.5 bg-linear-to-r from-accent/0 via-accent/50 to-accent/0 rounded-2xl opacity-0 group-hover:opacity-100 blur transition-all duration-500"></div>

              <div className="relative px-6 py-5 rounded-2xl bg-card/40 backdrop-blur-xl border border-border/40 hover:border-accent/50 hover:bg-card/60 transition-all duration-500 text-center h-full flex flex-col justify-center gap-2 group-hover:scale-105 group-hover:shadow-lg">
                <div className="text-3xl mb-2 group-hover:scale-110 transition-transform duration-300">{item.icon}</div>
                <div className="text-base font-bold text-foreground group-hover:text-accent transition-colors">{item.label}</div>
                <div className="text-xs text-muted-foreground leading-relaxed">{item.desc}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom CTA Section */}
        <div className="mt-20 text-center">
          <p className="text-sm text-muted-foreground">
            Powered by advanced AI • Trusted by creative professionals
          </p>
        </div>
      </div>
    </div>
  )
}
