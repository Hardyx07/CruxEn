"use client"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Button as StatefulButton } from "@/components/ui/stateful-button"
import { CopyButton } from "@/components/animate-ui/components/buttons/copy"
import { Card } from "@/components/ui/card"
import FrameworkSelector from "./framework-selector"
import PromptInput from "./prompt-input"
import { optimizePrompt } from "@/lib/api-client"
import ReactMarkdown from 'react-markdown'
import SpotlightCard from "./ui/SpotlightCard"

export default function PromptEnhancer() {
  const [rawPrompt, setRawPrompt] = useState("")
  const [enhancedPrompt, setEnhancedPrompt] = useState("")
  const [selectedUseCase, setSelectedUseCase] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [showTransform, setShowTransform] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [originalRawPrompt, setOriginalRawPrompt] = useState("")
  const promptBoxRef = useRef<HTMLDivElement>(null)

  const handleEnhance = async (promptToEnhance?: string, useCase?: string) => {
    const promptText = promptToEnhance ?? rawPrompt
    const selectedFramework = useCase ?? selectedUseCase

    if (!promptText.trim() || !selectedFramework) return

    setIsLoading(true)
    setShowTransform(true)
    setError(null)

    try {
      const response = await optimizePrompt(promptText, selectedFramework)

      if (response.error) {
        throw new Error(response.error)
      }

      setTimeout(() => {
        setEnhancedPrompt(response.optimized_prompt)
        setOriginalRawPrompt(promptText)
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

  const handleRetry = () => {
    if (originalRawPrompt && selectedUseCase) {
      handleEnhance(originalRawPrompt, selectedUseCase)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 py-16 relative z-10">
      {/* Hero Section with Modern Typography */}
      <div className="mb-20 text-center max-w-5xl mx-auto space-y-8">
        <div className="mb-4">
          <span className="text-xs font-semibold text-muted-foreground tracking-[0.3em] uppercase">For people who think faster than they type</span>
        </div>

        <h1 className="text-6xl md:text-7xl lg:text-[8rem] font-light mb-8 text-foreground tracking-tight leading-[0.95] font-serif">
         You Know the Idea CruxEn Finds the Words
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

        {/* Popular Frameworks Quick Select */}
        <div className="space-y-4">
          <div className="text-center">
            <span className="text-xs font-semibold text-muted-foreground tracking-[0.2em] uppercase">
              Popular Frameworks
            </span>
          </div>
          <div className="flex items-center justify-center gap-4">
            <button
              onClick={() => setSelectedUseCase("coding_technical")}
              className={`group relative px-8 py-4 rounded-xl backdrop-blur-xl border transition-all duration-300 ${
                selectedUseCase === "coding_technical"
                  ? "bg-accent/20 border-accent/50 shadow-lg shadow-accent/20"
                  : "bg-card/30 border-border/50 hover:border-accent/30 hover:bg-card/40"
              }`}
            >
              <div className="flex items-center gap-3">
                <svg className={`w-5 h-5 transition-colors duration-300 ${
                  selectedUseCase === "coding_technical" ? "text-accent" : "text-muted-foreground group-hover:text-accent/70"
                }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
                <span className={`font-medium transition-colors duration-300 ${
                  selectedUseCase === "coding_technical" ? "text-accent" : "text-foreground group-hover:text-accent/70"
                }`}>
                  Coding
                </span>
              </div>
            </button>

            <button
              onClick={() => setSelectedUseCase("research_exploration")}
              className={`group relative px-8 py-4 rounded-xl backdrop-blur-xl border transition-all duration-300 ${
                selectedUseCase === "research_exploration"
                  ? "bg-accent/20 border-accent/50 shadow-lg shadow-accent/20"
                  : "bg-card/30 border-border/50 hover:border-accent/30 hover:bg-card/40"
              }`}
            >
              <div className="flex items-center gap-3">
                <svg className={`w-5 h-5 transition-colors duration-300 ${
                  selectedUseCase === "research_exploration" ? "text-accent" : "text-muted-foreground group-hover:text-accent/70"
                }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span className={`font-medium transition-colors duration-300 ${
                  selectedUseCase === "research_exploration" ? "text-accent" : "text-foreground group-hover:text-accent/70"
                }`}>
                  Research
                </span>
              </div>
            </button>
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
                  {/* Result Header with Icon and Copy Button */}
                  <div className="flex items-center justify-between gap-3 mb-6 pb-6 border-b border-accent/20">
                    <div className="flex items-center gap-3">
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
                    <CopyButton
                      content={enhancedPrompt}
                      variant="outline"
                      size="lg"
                      className="w-14 min-w-14 border-2 border-accent/50 bg-card/50 hover:bg-accent/20 hover:border-accent text-accent rounded-xl backdrop-blur-sm transition-all duration-300 shadow-md hover:shadow-lg hover:shadow-accent/20 [&_svg]:size-5 cursor-pointer"
                    />
                  </div>

                  {/* Enhanced Prompt Display */}
                  <div className="relative">
                    <div className="absolute -left-4 top-0 bottom-0 w-1 bg-linear-to-b from-accent via-accent/60 to-transparent rounded-full"></div>
                    <div className="text-foreground text-lg md:text-xl leading-relaxed font-light pl-4 prose prose-invert max-w-none">
                      <ReactMarkdown>{enhancedPrompt}</ReactMarkdown>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex gap-4 pt-4 items-stretch h-14">
                    <Button
                      onClick={handleRetry}
                      disabled={isLoading}
                      className="px- nded-xl backdrop cursor-pointer h-full"
                    >
                      <span className="flex items-center justify-center gap-2">
                        
                        Retry
                      </span>
                    </Button>
                    <Button
                      onClick={() => {
                        setEnhancedPrompt("")
                        setRawPrompt("")
                        setOriginalRawPrompt("")
                      }}
                      className="flex-1 bg-linear-to-r from-accent to-accent/85 text-accent-foreground font-semibold rounded-xl shadow-lg shadow-accent/25 hover:shadow-xl hover:shadow-accent/35 transition-all duration-300 hover:brightness-110 cursor-pointer h-full"
                    >
                      <span className="flex items-center justify-center gap-2">
                        <span className="text-lg">🪄</span>
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
                  <StatefulButton
                    onClick={() => handleEnhance()}
                    disabled={!rawPrompt.trim() || !selectedUseCase || isLoading}
                    className="w-full mt-8 bg-linear-to-r from-accent via-accent/90 to-accent/80 hover:ring-accent text-accent-foreground font-bold py-4 rounded-xl cursor-pointer"
                  >
                    <span className="flex items-center justify-center gap-2">
                      {/* <span className="text-xl">🌀</span> */}
                      <span className="font-bold">Enhance </span>
                      <span className="text-xl">🪄</span>
                    </span>
                  </StatefulButton>
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

        {/* Why Creators Choose Cruxen Section */}
        <div className="mt-20 mb-12 text-center">
          <h2 className="text-2xl md:text-3xl font-light text-foreground mb-16 tracking-wide">
            Why Creators Use Cruxen Instead of Writing Prompts Alone
          </h2>
          
          {/* Premium Feature Cards with SpotlightCard */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {[
              { 
                title: "Adaptive AI Engine", 
                desc: "Learns and adapts to your unique style and requirements", 
                icon: (
                  <svg className="w-8 h-8 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                )
              },
              { 
                title: "Human-Style Understanding", 
                desc: "Interprets context and nuance like a creative partner", 
                icon: (
                  <svg className="w-8 h-8 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                )
              },
              { 
                title: "Zero Overthinking Required", 
                desc: "Just share your idea - we handle the complexity", 
                icon: (
                  <svg className="w-8 h-8 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                )
              }
            ].map((feature, index) => (
              <SpotlightCard 
                key={feature.title}
                className="group cursor-pointer transition-all duration-300 hover:scale-[1.02]"
                spotlightColor="rgba(139, 92, 246, 0.15)"
              >
                <div className="text-center space-y-4 p-4">
                  <div className="flex justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                    {feature.icon}
                  </div>
                  <h3 className="text-lg font-semibold text-foreground">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed group-hover:text-muted-foreground/90 transition-colors duration-300">
                    {feature.desc}
                  </p>
                </div>
              </SpotlightCard>
            ))}
          </div>
        </div>

        {/* Bottom CTA Section */}
        <div className="mt-20 text-center">
          <div className="inline-flex items-center gap-2 text-sm text-muted-foreground">
            <span>Powered by</span>
            <a 
              href="https://groq.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 group hover:text-accent transition-colors duration-300"
            >
              <span className="font-semibold">Groq</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
