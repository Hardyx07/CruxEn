"use client"

type Framework = "coding" | "research" | "study" | "business"

interface FrameworkSelectorProps {
  framework: Framework
  onFrameworkChange: (framework: Framework) => void
}

const frameworks: { value: Framework; label: string; icon: string; description: string }[] = [
  {
    value: "coding",
    label: "Coding",
    icon: "⚙️",
    description: "Programming tasks",
  },
  {
    value: "research",
    label: "Research",
    icon: "🔬",
    description: "Academic work",
  },
  {
    value: "study",
    label: "Study",
    icon: "📖",
    description: "Learning goals",
  },
  {
    value: "business",
    label: "Business",
    icon: "💼",
    description: "Professional tasks",
  },
]

export default function FrameworkSelector({ framework, onFrameworkChange }: FrameworkSelectorProps) {
  return (
    <div className="space-y-4">
      <label className="text-sm font-semibold text-foreground uppercase tracking-wide">Enhancement Framework</label>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {frameworks.map((fw) => (
          <button
            key={fw.value}
            onClick={() => onFrameworkChange(fw.value)}
            className={`relative p-4 rounded-lg transition-all duration-300 group ${
              framework === fw.value
                ? "bg-accent/20 border-2 border-accent shadow-lg shadow-accent/20"
                : "bg-card/30 border border-border/50 hover:border-accent/30 hover:bg-card/50"
            }`}
          >
            <div className="flex flex-col items-center gap-2">
              <span className="text-3xl">{fw.icon}</span>
              <span className="text-sm font-semibold text-foreground">{fw.label}</span>
              <span className="text-xs text-muted-foreground group-hover:text-accent/70 transition-colors">
                {fw.description}
              </span>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
