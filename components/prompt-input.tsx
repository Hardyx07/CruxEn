"use client"

import { useState } from "react"

interface PromptInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
}

export default function PromptInput({ value, onChange, placeholder = "Enter your prompt..." }: PromptInputProps) {
  const [isFocused, setIsFocused] = useState(false)
  const maxLength = 2000
  const charCount = value.length
  const charPercentage = (charCount / maxLength) * 100

  return (
    <div className="relative">
      {/* Floating label */}
      <label 
        className={`absolute left-6 transition-all duration-300 pointer-events-none ${
          isFocused || value 
            ? '-top-3 text-xs font-semibold text-accent bg-card px-2 rounded-full' 
            : 'top-4 text-base text-muted-foreground/60'
        }`}
      >
        {isFocused || value ? 'Your Prompt' : placeholder}
      </label>

      {/* Glow effect on focus */}
      {isFocused && (
        <div className="absolute -inset-0.5 bg-linear-to-r from-accent/30 via-primary/20 to-accent/30 rounded-2xl blur opacity-50 animate-pulse"></div>
      )}

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        maxLength={maxLength}
        className="relative w-full px-6 pt-6 pb-4 bg-background/60 backdrop-blur-xl border-2 border-border/60 rounded-2xl text-foreground text-lg placeholder:text-transparent focus:outline-none focus:border-accent/60 focus:bg-background/80 resize-none transition-all duration-500 focus:shadow-lg focus:shadow-accent/10 leading-relaxed"
        rows={8}
      />

      {/* Character counter with progress bar */}
      <div className="flex items-center justify-between mt-3 px-2">
        <div className="flex-1 h-1.5 bg-border/30 rounded-full overflow-hidden mr-4">
          <div 
            className={`h-full transition-all duration-300 rounded-full ${
              charPercentage > 90 ? 'bg-destructive' : charPercentage > 70 ? 'bg-chart-4' : 'bg-accent'
            }`}
            style={{ width: `${charPercentage}%` }}
          />
        </div>
        <span className={`text-xs font-medium transition-colors ${
          charPercentage > 90 ? 'text-destructive' : charPercentage > 70 ? 'text-chart-4' : 'text-muted-foreground'
        }`}>
          {charCount} / {maxLength}
        </span>
      </div>

      {/* Quick tips on focus */}
      {isFocused && !value && (
        <div className="mt-4 p-3 bg-accent/5 border border-accent/20 rounded-lg text-xs text-muted-foreground space-y-1 animate-fade-in">
          <div className="font-semibold text-accent mb-1">💡 Pro Tips:</div>
          <div>• Be specific about your desired outcome</div>
          <div>• Include relevant context and constraints</div>
          <div>• Mention your target audience if applicable</div>
        </div>
      )}
    </div>
  )
}
