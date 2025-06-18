from google.adk.agents import Agent

structural_notes_agent = Agent(
    name="StructuralNotesAgent",
    model="gemini-2.0-flash",
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

Extract the following fields:
- Load types considered
- Span and layout summary
- Design codes used (e.g., IRC 6, IS 456, IS 1343)
- Concrete and steel grades assumed
- Design approach
- Structural system overview
- Construction stages (if any)
- Notes or warnings (e.g., seismic detailing, corrosion zones, exposure class)

Return in this format:
```json
{
  "structural_notes": {
    "load_types": ["Dead Load", "Live Load (IRC Class A)", "Seismic Load"],
    "span_arrangement": "4 x 32m = 128m",
    "design_method": "Limit State Method",
    "design_codes": ["IS 456", "IRC 6", "IS 1343"],
    "concrete_grades": ["M40", "M50"],
    "steel_grades": ["Fe500D", "Fe415"],
    "structural_system": "PSC Box Girders on Pile Foundation",
    "construction_stages": "Two-stage deck casting with temporary bearings",
    "special_notes": ["Seismic Zone III", "Wind Zone V", "Exposure Class 'Severe'"]
  }
}
If a value is not mentioned in the document, return "N/A". Group similar items and avoid duplication.
""",
    output_key="structural_notes"
        )