from google.adk.agents import Agent

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