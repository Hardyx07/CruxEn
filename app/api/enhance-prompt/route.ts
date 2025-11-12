import { type NextRequest, NextResponse } from "next/server"

const GEMINI_API_KEY = process.env.GEMINI_API_KEY
const GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

const frameworkPrompts = {
  coding: `You are an expert coding prompt engineer. Transform the user's raw idea into a professional, detailed coding prompt that:
- Clearly specifies the programming language and framework
- Includes specific requirements and constraints
- Mentions expected output format
- Suggests best practices and patterns
- Is concise but comprehensive`,

  research: `You are an expert research prompt engineer. Transform the user's raw idea into an academic research prompt that:
- Uses formal and scholarly language
- Specifies the research methodology
- Includes key concepts and terminology
- Defines scope and limitations
- Suggests credible sources and approaches`,

  study: `You are an expert educational prompt engineer. Transform the user's raw idea into an effective study prompt that:
- Breaks down complex concepts into understandable parts
- Includes learning objectives
- Suggests interactive learning methods
- Provides practical examples
- Encourages deeper understanding`,

  business: `You are an expert business prompt engineer. Transform the user's raw idea into a professional business prompt that:
- Uses corporate and professional language
- Includes clear business objectives
- Mentions ROI, metrics, and KPIs
- Suggests strategic approaches
- Is action-oriented and results-focused`,
}

export async function POST(request: NextRequest) {
  try {
    const { prompt, framework } = await request.json()

    if (!prompt || !framework) {
      return NextResponse.json({ error: "Missing prompt or framework" }, { status: 400 })
    }

    if (!GEMINI_API_KEY) {
      return NextResponse.json({ error: "GEMINI_API_KEY environment variable not set" }, { status: 500 })
    }

    const systemPrompt = frameworkPrompts[framework as keyof typeof frameworkPrompts]
    if (!systemPrompt) {
      return NextResponse.json({ error: "Invalid framework" }, { status: 400 })
    }

    const requestBody = {
      contents: [
        {
          parts: [
            {
              text: `${systemPrompt}\n\nUser's raw prompt: "${prompt}"\n\nProvide only the enhanced prompt without any explanation or preamble.`,
            },
          ],
        },
      ],
      generationConfig: {
        temperature: 0.7,
        topK: 40,
        topP: 0.95,
        maxOutputTokens: 500,
      },
    }

    const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    })

    if (!response.ok) {
      const errorData = await response.json()
      console.error("Gemini API Error:", errorData)
      return NextResponse.json({ error: "Failed to enhance prompt with Gemini API" }, { status: response.status })
    }

    const data = await response.json()
    const enhanced = data.candidates?.[0]?.content?.parts?.[0]?.text || "Failed to generate enhanced prompt"

    return NextResponse.json({ enhanced })
  } catch (error) {
    console.error("API Error:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
