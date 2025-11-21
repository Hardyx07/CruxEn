"use client"

import { useEffect, useState, useRef } from "react"
import type { UseCase } from "@/lib/api-client"
import { fetchUseCases } from "@/lib/api-client"
import "./framework-selector.css"

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
  const [selectedLabel, setSelectedLabel] = useState<string>("Select Option")
  
  // Animation states
  const [isOpen, setIsOpen] = useState(false)
  const [textClass, setTextClass] = useState("")
  const [flashClass, setFlashClass] = useState("")
  const [searchQuery, setSearchQuery] = useState("")
  
  const dropdownRef = useRef<HTMLDivElement>(null)

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
        } else if (selectedUseCase) {
            const found = cases.find(c => c.subcategory === selectedUseCase)
            if (found) {
                setSelectedLabel(`${found.subcategory.replace(/_/g, " ")} - ${found.description}`)
            }
        }
      } catch (err) {
        console.error("Failed to load use cases:", err)
        setError("Failed to load categories")
        setLoading(false)
      }
    }

    loadUseCases()
  }, [selectedUseCase, onUseCaseChange])

  // Close on outside click
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  const handleSelect = (useCase: UseCase) => {
    const newLabel = `${useCase.subcategory.replace(/_/g, " ")} - ${useCase.description}`
    
    if (newLabel === selectedLabel) {
        setIsOpen(false)
        return
    }

    // A. Trigger Exit Animation
    setTextClass("text-out")
    
    // B. Trigger Container Glow
    setFlashClass("flash-glow")

    // C. Swap Text mid-animation
    setTimeout(() => {
        onUseCaseChange(useCase.subcategory)
        setSelectedLabel(newLabel)
        
        // Remove Exit class, Add Enter class
        setTextClass("text-in")
    }, 350)

    // D. Clean up Animation classes
    setTimeout(() => {
        setTextClass("")
        setFlashClass("")
    }, 750)

    setIsOpen(false)
  }

  // Filter use cases based on search
  const filteredUseCases = useCases.filter(uc => 
    uc.subcategory.toLowerCase().includes(searchQuery.toLowerCase()) ||
    uc.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
    uc.category.toLowerCase().includes(searchQuery.toLowerCase())
  )

  // Group use cases by category
  const groupedByCat = filteredUseCases.reduce(
    (acc, uc) => {
      if (!acc[uc.category]) {
        acc[uc.category] = []
      }
      acc[uc.category].push(uc)
      return acc
    },
    {} as Record<string, UseCase[]>
  )

  if (error) {
    return (
      <div className="p-4 bg-destructive/10 border border-destructive/30 rounded-lg text-sm text-destructive">
        {error}
      </div>
    )
  }

  return (
    <div className="glass-dropdown" ref={dropdownRef}>
        <div 
            className={`glass-select ${flashClass}`} 
            onClick={() => setIsOpen(!isOpen)}
        >
            <div className="glass-text-wrapper">
                <span className={`glass-selected-text ${textClass}`}>
                    {loading ? "Loading..." : selectedLabel}
                </span>
            </div>
            <div className={`glass-caret ${isOpen ? "glass-caret-rotate" : ""}`}></div>
        </div>
        
        <ul className={`glass-menu ${isOpen ? "glass-menu-open" : ""}`}>
            <li className="glass-menu-search">
                <input
                    type="text"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white placeholder:text-gray-400 focus:outline-none focus:border-white/20 transition-colors"
                    onClick={(e) => e.stopPropagation()}
                />
            </li>
            
            {Object.entries(groupedByCat).length > 0 ? (
                <>
                    {Object.entries(groupedByCat).map(([category, items]) => (
                        <li key={category} style={{ listStyle: 'none' }}>
                            <div className="glass-menu-category">{category}</div>
                            {items.map((useCase) => (
                                <div 
                                    key={useCase.subcategory}
                                    className={`glass-menu-item ${selectedUseCase === useCase.subcategory ? "active" : ""}`}
                                    onClick={() => handleSelect(useCase)}
                                >
                                    {useCase.subcategory.replace(/_/g, " ")} - {useCase.description}
                                </div>
                            ))}
                        </li>
                    ))}
                </>
            ) : (
                <li className="p-4 text-center text-sm text-gray-400" style={{ listStyle: 'none' }}>
                    No results found
                </li>
            )}
        </ul>
    </div>
  )
}
