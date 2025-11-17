"use client"

import { useEffect, useState } from "react"
import type { UseCase } from "@/lib/api-client"
import { fetchUseCases } from "@/lib/api-client"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
  DropdownMenuLabel,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"

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
  const [selectedLabel, setSelectedLabel] = useState<string>("Select a category")
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    const loadUseCases = async () => {
      try {
        setLoading(false)
        const cases = await fetchUseCases()
        setUseCases(cases)
        if (cases.length > 0 && !selectedUseCase) {
          const firstCase = cases[0]
          onUseCaseChange(firstCase.subcategory)
          setSelectedLabel(
            `${firstCase.subcategory.replace(/_/g, " ")} - ${firstCase.description}`
          )
        }
      } catch (err) {
        console.error("Failed to load use cases:", err)
        setError("Failed to load categories")
        setLoading(false)
      }
    }

    loadUseCases()
  }, [selectedUseCase, onUseCaseChange])

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

  const handleSelect = (useCase: UseCase) => {
    onUseCaseChange(useCase.subcategory)
    setSelectedLabel(
      `${useCase.subcategory.replace(/_/g, " ")} - ${useCase.description}`
    )
  }

  if (error) {
    return (
      <div className="p-4 bg-destructive/10 border border-destructive/30 rounded-lg text-sm text-destructive">
        {error}
      </div>
    )
  }

  const [searchQuery, setSearchQuery] = useState("")

  // Filter use cases based on search
  const filteredUseCases = useCases.filter(uc => 
    uc.subcategory.toLowerCase().includes(searchQuery.toLowerCase()) ||
    uc.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
    uc.category.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const filteredGrouped = filteredUseCases.reduce(
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
    <div className="space-y-3 relative z-40">
      <div className="flex items-center justify-between">
        <label className="text-sm font-bold text-foreground uppercase tracking-wider flex items-center gap-2">
          <svg className="w-4 h-4 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
          Enhancement Category
        </label>
        {selectedUseCase && (
          <span className="text-xs font-medium text-accent bg-accent/10 px-3 py-1 rounded-full">
            Selected
          </span>
        )}
      </div>
      <DropdownMenu open={isOpen} onOpenChange={setIsOpen}>
        <DropdownMenuTrigger asChild>
          <Button
            variant="outline"
            className="w-full justify-between bg-background/60 backdrop-blur-xl border-2 border-border/60 hover:border-accent/50 hover:bg-background/80 transition-all duration-300 py-6 text-base font-medium hover:shadow-lg group"
            disabled={loading}
          >
            <span className="text-left truncate flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-accent animate-pulse"></span>
              {selectedLabel}
            </span>
            <svg className="w-5 h-5 transition-transform duration-300 group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent 
          align="start" 
          sideOffset={12}
          className="w-[calc(100vw-2rem)] md:w-[680px] max-h-[75vh] overflow-hidden bg-card/95 backdrop-blur-2xl border-2 border-accent/30 rounded-2xl shadow-2xl shadow-accent/20 p-0"
        >
          {/* Search Bar */}
          <div className="sticky top-0 z-10 p-4 bg-card/95 backdrop-blur-xl border-b border-border/50">
            <div className="relative">
              <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                placeholder="Search categories..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-background/60 border border-border/50 rounded-xl text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-accent/50 focus:ring-2 focus:ring-accent/20 transition-all duration-300"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery("")}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
            <div className="mt-2 text-xs text-muted-foreground flex items-center gap-2">
              <span>{filteredUseCases.length} {filteredUseCases.length === 1 ? 'category' : 'categories'} found</span>
            </div>
          </div>

          {/* Scrollable Content */}
          <div className="overflow-y-auto max-h-[calc(75vh-120px)] p-4">
            {Object.entries(filteredGrouped).length > 0 ? (
              Object.entries(filteredGrouped).map(([category, cases], catIndex) => (
                <div key={category} className="mb-6 last:mb-0">
                  <DropdownMenuLabel className="text-xs font-bold uppercase tracking-wider text-accent mb-3 flex items-center gap-2 px-2">
                    <div className="w-1 h-4 bg-accent rounded-full"></div>
                    {category.replace(/_/g, " ")}
                  </DropdownMenuLabel>
                  <div className="space-y-2">
                    {cases.map((useCase, index) => (
                      <DropdownMenuItem
                        key={useCase.subcategory}
                        onClick={() => {
                          handleSelect(useCase)
                          setIsOpen(false)
                          setSearchQuery("")
                        }}
                        className={`flex flex-col items-start p-4 cursor-pointer rounded-xl transition-all duration-300 group border ${
                          selectedUseCase === useCase.subcategory
                            ? "bg-accent/10 border-accent/60 shadow-lg shadow-accent/10"
                            : "bg-background/20 border-border/30 hover:bg-accent/5 hover:border-accent/40"
                        }`}
                        style={{ animationDelay: `${index * 30}ms` }}
                      >
                        <div className="flex items-start justify-between w-full gap-3">
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-1">
                              <span className={`font-semibold capitalize text-base transition-colors ${
                                selectedUseCase === useCase.subcategory ? "text-accent" : "text-foreground/90 group-hover:text-accent"
                              }`}>
                                {useCase.subcategory.replace(/_/g, " ")}
                              </span>
                              {selectedUseCase === useCase.subcategory && (
                                <svg className="w-5 h-5 text-accent flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                              )}
                            </div>
                            <span className="text-sm text-muted-foreground leading-relaxed block break-words">
                              {useCase.description}
                            </span>
                            {useCase.role && (
                              <div className="mt-2 inline-flex items-center gap-1 text-xs text-accent/80 bg-accent/10 px-2 py-1 rounded-md">
                                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                                {useCase.role}
                              </div>
                            )}
                          </div>
                        </div>
                      </DropdownMenuItem>
                    ))}
                  </div>
                  {catIndex < Object.entries(filteredGrouped).length - 1 && (
                    <DropdownMenuSeparator className="my-4" />
                  )}
                </div>
              ))
            ) : (
              <div className="text-center py-12">
                <svg className="w-16 h-16 mx-auto text-muted-foreground/30 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-muted-foreground text-sm">No categories found matching "{searchQuery}"</p>
                <button
                  onClick={() => setSearchQuery("")}
                  className="mt-4 text-sm text-accent hover:text-accent/80 transition-colors"
                >
                  Clear search
                </button>
              </div>
            )}
          </div>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
