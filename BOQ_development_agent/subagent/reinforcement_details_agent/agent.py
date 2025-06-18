from google.adk.agents import Agent

reinforcement_details_agent = Agent(
    name="ReinforcementDetailsAgent",
    model="gemini-2.0-flash",
    description="Extracts detailed reinforcement specifications and quantities from bridge design documents, including bar sizes, spacing, placement, and computes steel quantities where possible.",
    instruction="""
You will receive a bridge design PDF (GAD or structural drawing).

Your task is to extract reinforcement details for the following components (if present):
- Piers
- Abutments
- Deck Slab
- Girders
- Pile Caps
- Piles
- Crash Barriers
- Cross Girders
- Seismic stoppers

Extract the following fields for each:
- Component name
- Bar type and grade (e.g., Fe500D)
- Bar diameter (mm)
- Number of bars
- Bar spacing (e.g., 150mm c/c)
- Bar placement (Top, Bottom, Side)
- Lap length or anchorage
- Cover (mm)
- (Optional) compute approximate total weight using:  
  **Weight (kg) ≈ (D² / 162) × Length × No. of bars**

Return in this format:
```json
{
  "reinforcement_details": [
    {
      "component": "Deck Slab",
      "bar_grade": "Fe550D",
      "bar_diameter_mm": 16,
      "spacing_mm": 150,
      "placement": "Top & Bottom",
      "cover_mm": 50,
      "lap_length_mm": 800,
      "bar_count": 120,
      "approx_steel_weight_kg": 1520
    }
  ]
}
If any value is missing, return as "N/A" and annotate if assumptions are made.
""",
    output_key="reinforcement_details"
    )