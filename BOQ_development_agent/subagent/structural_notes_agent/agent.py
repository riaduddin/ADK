from google.adk.agents import Agent
from pydantic import BaseModel, Field


class StructuralNotes(BaseModel):
    load_types: str = Field(description="Comma-separated load types considered (e.g., Dead Load, IRC Class A, Seismic Load)")
    span_arrangement: str = Field(description="Span layout summary (e.g., 4 x 32m = 128m) or 'N/A'")
    design_method: str = Field(description="Design methodology used (e.g., Limit State Method) or 'N/A'")
    design_codes: str = Field(description="Comma-separated design codes (e.g., IS 456, IRC 6, IS 1343) or 'N/A'")
    concrete_grades: str = Field(description="Comma-separated concrete grades used (e.g., M40, M50) or 'N/A'")
    steel_grades: str = Field(description="Comma-separated steel grades used (e.g., Fe500D, Fe415) or 'N/A'")
    structural_system: str = Field(description="Structural system overview (e.g., RCC, PSC, pile foundation) or 'N/A'")
    construction_stages: str = Field(description="Construction phasing or sequence, or 'N/A'")
    special_notes: str = Field(description="Special notes like seismic detailing, corrosion warnings, etc. or 'N/A'")


class StructuralNotesOutput(BaseModel):
    structural_notes: StructuralNotes


structural_notes_agent = Agent(
    name="StructuralNotesAgent",
    model="gemini-2.5-pro",
    description="Extracts structural engineering notes from bridge designs, including loading criteria, design assumptions, member specifications, and special construction instructions.",
    instruction="""
You will receive a structural or GAD (General Arrangement Drawing) PDF of a bridge design.

Your task is to extract all structural notes and design assumptions related to:

- Loads considered (e.g., Dead Load, Live Load, IRC Class A, Seismic Load)
- Design methodology (e.g., Limit State Method, Working Stress Method)
- Structural system (e.g., RCC deck, PSC girders, pile foundation)
- Span arrangement (e.g., 4 x 32m = 128m total)
- Material assumptions (e.g., Concrete M45, Fe550D Steel)
- Foundation system and substructure type
- Prestressing or post-tensioning details (if mentioned)
- Any special instructions, restrictions, or staged construction notes

Return only valid JSON in this format:
{
  "structural_notes": {
    "load_types": "Dead Load, Live Load (IRC Class A), Seismic Load",
    "span_arrangement": "4 x 32m = 128m",
    "design_method": "Limit State Method",
    "design_codes": "IS 456, IRC 6, IS 1343",
    "concrete_grades": "M40, M50",
    "steel_grades": "Fe500D, Fe415",
    "structural_system": "PSC Box Girders on Pile Foundation",
    "construction_stages": "Two-stage deck casting with temporary bearings",
    "special_notes": "Seismic Zone III, Wind Zone V, Exposure Class 'Severe'"
  }
}

Use "N/A" for missing data. Combine related values into comma-separated strings.
""",
    output_schema=StructuralNotesOutput,
    output_key="structural_notes"
)
