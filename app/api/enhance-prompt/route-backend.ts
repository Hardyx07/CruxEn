import { type NextRequest, NextResponse } from "next/server"

// Point this to your Python backend
const BACKEND_API_URL = process.env.BACKEND_API_URL || "http://localhost:5000"

export async function POST(request: NextRequest) {
  try {
    const { prompt, framework } = await request.json()

    if (!prompt || !framework) {
      return NextResponse.json({ error: "Missing prompt or framework" }, { status: 400 })
    }

    // Forward request to Python backend
    const backendResponse = await fetch(`${BACKEND_API_URL}/api/enhance-prompt`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt,
        framework,
      }),
    })

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json()
      return NextResponse.json(
        { error: errorData.error || "Backend error" },
        { status: backendResponse.status }
      )
    }

    const data = await backendResponse.json()

    return NextResponse.json({
      enhanced: data.enhanced,
      framework: data.framework,
      success: data.success,
    })
  } catch (error) {
    console.error("Error enhancing prompt:", error)
    return NextResponse.json(
      { error: "Failed to enhance prompt. Make sure the backend is running." },
      { status: 500 }
    )
  }
}
