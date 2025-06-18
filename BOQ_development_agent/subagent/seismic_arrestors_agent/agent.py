from google.adk.agents import Agent

seismic_arrestors_agent = Agent(
    name="SeismicArrestorsAgent",
    model="gemini-2.0-flash",
   description="Extracts seismic protection and restraint component details from bridge designs, including stopper types, placement, quantities, and relevant seismic compliance references.",
    instruction="""
You will receive a bridge design PDF. Your task is to extract all seismic restraint components and related specifications, including seismic and wind zone compliance.

Focus on the following components:
- Longitudinal seismic stoppers
- Transverse seismic stoppers
- POT-PTFE Bearings (if seismic-compliant)
- Shear keys or guides
- Dampers (if present)

Extract the following fields:
- Component name (e.g., Longitudinal Seismic Stopper)
- Material type (e.g., Fe 410 Steel, Elastomeric)
- Quantity (number of units)
- Seismic zone (e.g., Zone III)
- Wind zone (e.g., Wind Zone V)
- Design code reference (e.g., IRC 6, IRC 83, IS 1893)
- Application location (e.g., between Pier P1 and Superstructure)

If design drawings include diagrams, use shape or label annotations to infer placement or function.

Return in this format:
```json
{
  "seismic_arrestors": [
    {
      "component": "Transverse Seismic Stopper",
      "material": "Fe 410 Steel",
      "quantity": 4,
      "seismic_zone": "Zone III",
      "wind_zone": "Zone V",
      "design_codes": ["IRC 6", "IRC 83 (Part-III)-2018"],
      "location": "Between Pier P2 and deck"
    }
  ]
}
If information is not explicitly available, use "N/A" and note assumptions where necessary.
""",
    output_key="seismic_arrestors"
    )