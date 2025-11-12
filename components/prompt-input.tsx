"use client"

interface PromptInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
}

export default function PromptInput({ value, onChange, placeholder = "Enter your prompt..." }: PromptInputProps) {
  return (
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full px-6 py-4 bg-background/50 border border-border/60 rounded-lg text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/30 resize-none transition-all duration-300 focus:bg-background/70"
      rows={7}
    />
  )
}
