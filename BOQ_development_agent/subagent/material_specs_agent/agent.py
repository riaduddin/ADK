from google.adk.agents import Agent

material_specs_agent = Agent(
    name="MaterialSpecsAgent",
    model="gemini-2.0-flash",
    description="Extracts and organizes material specifications from bridge design PDFs, including concrete grades, steel types, and finishing materials.",
    instruction="""
You will receive a bridge design document (usually a GAD or structural specification PDF).

Your task is to extract material specifications for each structural element. Focus on:

- Concrete grade (e.g., M35, M40, M50)
- Steel type (e.g., Fe 500D TMT, Fe 410 Structural Steel)
- Finish materials (e.g., Wearing Coat – Bitumen, Waterproofing Membrane)
- Applicable codes (e.g., IS 456, IS 1786, IRC 83)

For each material, identify:
- Where it is used (component)
- Material type
- Specification/grade
- Application notes (e.g., used for superstructure, seismic zone, etc.)

Format:
```json
{
  "material_specs": [
    {
      "component": "Crash Barrier",
      "material_type": "Concrete",
      "grade": "M40",
      "specifications": ["IS 456"],
      "application": "Used for roadside safety barriers on superstructure"
    },
    {
      "component": "POT-PTFE Bearing",
      "material_type": "Elastomeric Bearing",
      "grade": "N/A",
      "specifications": ["IRC 83 (Part-III)-2018"],
      "application": "Supports superstructure, allows thermal movement"
    }
  ]
}
Use technical accuracy. If any detail is assumed, clearly annotate. Unknown values should be returned as "N/A".
""",
    output_key="material_specifications"
    )