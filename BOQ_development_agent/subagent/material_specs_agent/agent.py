<<<<<<< HEAD
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import List


class MaterialSpec(BaseModel):
    component: str = Field(description="Name of the component where the material is used (e.g., Crash Barrier, Deck Slab)")
    material_type: str = Field(description="Type of material (e.g., Concrete, Steel, Elastomeric Bearing)")
    grade: str = Field(description="Grade of material (e.g., M40, Fe 500D, or 'N/A')")
    specifications: List[str] = Field(description="Relevant codes or standards (e.g., IS 456, IRC 83)")
    application: str = Field(description="Where and how the material is used (e.g., Used for deck slab in seismic zones)")

class MaterialSpecsOutput(BaseModel):
    material_specs: List[MaterialSpec]


material_specs_agent = Agent(
    name="MaterialSpecsAgent",
    model="gemini-2.5-pro",
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

Return only valid **JSON**, no extra text.

Example format:
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

Use technical accuracy. If any value is unknown, use "N/A". If assumed, annotate in the application field.
""",
    output_schema=MaterialSpecsOutput,
    output_key="material_specs"
)
=======
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
>>>>>>> master
