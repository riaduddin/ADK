from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import List


class ReinforcementItem(BaseModel):
    component: str = Field(description="Name of the component (e.g., Deck Slab, Pier)")
    bar_grade: str = Field(description="Reinforcement bar grade (e.g., Fe500D)")
    bar_diameter_mm: str = Field(description="Bar diameter in mm or 'N/A'")
    spacing_mm: str = Field(description="Spacing between bars in mm or 'N/A'")
    placement: str = Field(description="Bar placement position (e.g., Top, Bottom, Side)")
    cover_mm: str = Field(description="Concrete cover in mm or 'N/A'")
    lap_length_mm: str = Field(description="Lap length or anchorage length in mm or 'N/A'")
    bar_count: str = Field(description="Number of bars or 'N/A'")
    approx_steel_weight_kg: str = Field(description="Approximate total weight in kg or 'N/A'")


class ReinforcementDetailsOutput(BaseModel):
    reinforcement_details: List[ReinforcementItem]


reinforcement_details_agent = Agent(
    name="ReinforcementDetailsAgent",
    model="gemini-2.5-pro",
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

Return result in valid JSON format only. No extra explanation or markdown.

Example:
{
  "reinforcement_details": [
    {
      "component": "Deck Slab",
      "bar_grade": "Fe550D",
      "bar_diameter_mm": "16",
      "spacing_mm": "150",
      "placement": "Top & Bottom",
      "cover_mm": "50",
      "lap_length_mm": "800",
      "bar_count": "120",
      "approx_steel_weight_kg": "1520"
    }
  ]
}

Use "N/A" for any unknown values. Add reasonable assumptions only if needed.
""",
    output_schema=ReinforcementDetailsOutput,
    output_key="reinforcement_details"
)
