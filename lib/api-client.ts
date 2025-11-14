/**
 * API client for backend communication
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"

export interface UseCase {
  category: string
  subcategory: string
  description: string
  frameworks: string[]
  role: string | null
}

export interface ChatResponse {
  optimized_prompt: string
  error?: string
  details?: string
}

/**
 * Fetch all available use cases from backend
 */
export async function fetchUseCases(): Promise<UseCase[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/use-cases`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error(`Failed to fetch use cases: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("Error fetching use cases:", error)
    return []
  }
}

/**
 * Send prompt to backend for optimization via Groq
 */
export async function optimizePrompt(
  prompt: string,
  useCase: string
): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt,
        use_case: useCase,
      }),
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(
        errorData.error || `Failed to optimize prompt: ${response.status}`
      )
    }

    return await response.json()
  } catch (error) {
    console.error("Error optimizing prompt:", error)
    throw error
  }
}
