"use client"

import { useEffect, useState } from "react"
import type { UseCase } from "@/lib/api-client"
import { fetchUseCases } from "@/lib/api-client"

interface FrameworkSelectorProps {
  selectedUseCase: string | null
  onUseCaseChange: (useCase: string) => void
}

export default function FrameworkSelector({
  selectedUseCase,
  onUseCaseChange,
}: FrameworkSelectorProps) {
  const [useCases, setUseCases] = useState<UseCase[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadUseCases = async () => {
      try {
        setLoading(true)
        const cases = await fetchUseCases()
        setUseCases(cases)
        if (cases.length > 0 && !selectedUseCase) {
          onUseCaseChange(cases[0].subcategory)
        }
      } catch (err) {
        console.error("Failed to load use cases:", err)
        setError("Failed to load categories")
      } finally {
        setLoading(false)
      }
    }

    loadUseCases()
  }, [selectedUseCase, onUseCaseChange])

  if (loading) {
    return (
      <div className="space-y-4">
        <label className="text-sm font-semibold text-foreground uppercase tracking-wide">
          Enhancement Framework
        </label>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[...Array(4)].map((_, i) => (
            <div
              key={i}
              className="h-24 rounded-lg bg-card/30 border border-border/50 animate-pulse"
            />
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-4 bg-destructive/10 border border-destructive/30 rounded-lg text-sm text-destructive">
        {error}
      </div>
    )
  }

  // Group use cases by category
  const groupedByCat = useCases.reduce(
    (acc, uc) => {
      if (!acc[uc.category]) {
        acc[uc.category] = []
      }
      acc[uc.category].push(uc)
      return acc
    },
    {} as Record<string, UseCase[]>
  )

  return (
    <div className="space-y-4">
      <label className="text-sm font-semibold text-foreground uppercase tracking-wide">
        Enhancement Framework
      </label>
      <div className="space-y-4">
        {Object.entries(groupedByCat).map(([category, cases]) => (
          <div key={category}>
            <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
              {category.replace(/_/g, " ")}
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {cases.map((uc) => (
                <button
                  key={uc.subcategory}
                  onClick={() => onUseCaseChange(uc.subcategory)}
                  className={`relative p-4 rounded-lg transition-all duration-300 group text-left h-full ${
                    selectedUseCase === uc.subcategory
                      ? "bg-accent/20 border-2 border-accent shadow-lg shadow-accent/20"
                      : "bg-card/30 border border-border/50 hover:border-accent/30 hover:bg-card/50"
                  }`}
                  title={uc.description}
                >
                  <div className="font-semibold text-foreground text-sm capitalize">
                    {uc.subcategory.replace(/_/g, " ")}
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">
                    {uc.description}
                  </div>
                  <div className="text-xs text-accent/70 mt-2">
                    {uc.frameworks.join(", ")}
                  </div>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
