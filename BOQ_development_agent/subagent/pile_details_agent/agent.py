<<<<<<< HEAD
from google.adk.agents import Agent
from pydantic import BaseModel, Field


class ReinforcementDetails(BaseModel):
    bar_grade: str = Field(description="Grade of reinforcement bars (e.g., Fe 550D or 'N/A')")
    bar_count: str = Field(description="Total number of bars used or 'N/A'")
    bar_diameter_mm: str = Field(description="Diameter of each bar in mm or 'N/A'")
    bar_spacing: str = Field(description="Spacing between bars in mm or 'N/A'")
    lap_length_mm: str = Field(description="Lap length of bars in mm or 'N/A'")


class PileDetails(BaseModel):
    pile_type: str = Field(description="Type of pile (e.g., Bored Cast-in-situ, Driven)")
    diameter_mm: str = Field(description="Pile diameter in mm or 'N/A'")
    length_m: str = Field(description="Pile length in meters or 'N/A'")
    count: str = Field(description="Number of piles or 'N/A'")
    total_volume_m3: str = Field(description="Computed total volume in m³ or 'N/A'")
    reinforcement: ReinforcementDetails


class PileDetailsOutput(BaseModel):
    pile_details: PileDetails


pile_details_agent = Agent(
    name="PileDetailsAgent",
    model="gemini-2.5-pro",
    description="Extracts details about pile dimensions, types, reinforcement, and computes total volume from the bridge drawing.",
    instruction="""
You will receive a bridge design PDF (GAD or similar).

Your task is to extract pile-related information:
- Pile type (e.g., Cast-in-situ, Bored, Driven)
- Diameter (mm)
- Length per pile (m)
- Number of piles
- Compute total concrete volume
- Extract reinforcement bar type, count, spacing
- Compute total weight (if data available)

Use:
- Volume = π × (D/2)^2 × H × count
- Weight = Length × unit weight per dia (use assumptions if not mentioned)

Return result in valid JSON format, **no extra text**.

Example:
{
  "pile_details": {
    "pile_type": "Bored Cast-in-situ",
    "diameter_mm": "1200",
    "length_m": "22.5",
    "count": "4",
    "total_volume_m3": "101.8",
    "reinforcement": {
      "bar_grade": "Fe 550D",
      "bar_count": "24",
      "bar_diameter_mm": "20",
      "bar_spacing": "N/A",
      "lap_length_mm": "1020"
    }
  }
}

Mark unknowns as "N/A". Use string values for all fields, including numbers.
""",
    output_schema=PileDetailsOutput,
    output_key="pile_details"
)
=======
from google.adk.agents import Agent

pile_details_agent = Agent(
    name="PileDetailsAgent",
    model="gemini-2.0-flash",
     description="Extracts details about pile dimensions, types, reinforcement, and computes total volume from the bridge drawing.",
    instruction="""
You will receive a bridge design PDF (GAD or similar).

Your task is to extract pile-related information:
- Pile type (e.g., Cast-in-situ, Bored, Driven)
- Diameter (mm)
- Length per pile (m)
- Number of piles
- Compute total concrete volume
- Extract reinforcement bar type, count, spacing
- Compute total weight (if data available)

Use:
- Volume = π × (D/2)^2 × H × count
- Weight = Length × unit weight per dia (use assumptions if not mentioned)

Return result in JSON format:
{
  "pile_details": {
    "pile_type": "Bored Cast-in-situ",
    "diameter_mm": 1200,
    "length_m": 22.5,
    "count": 4,
    "total_volume_m3": 101.8,
    "reinforcement": {
      "bar_grade": "Fe 550D",
      "bar_count": 24,
      "bar_diameter_mm": 20,
      "bar_spacing": "N/A",
      "lap_length_mm": 1020
    }
  }
}

Mark unknowns as `"N/A"` but include assumptions where applicable.
""",
    output_key="pile_details"
    )
>>>>>>> master
