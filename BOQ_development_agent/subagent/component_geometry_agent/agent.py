from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import List, Union

from pydantic import BaseModel, Field
from typing import List

class GeometryComponent(BaseModel):
    component: str = Field(description="Name of the structural component")
    shape: str = Field(description="Shape of the component (e.g., rectangle, slab, I-beam)")
    height_m: str = Field(description="Height in meters or 'N/A'")
    length_m: str = Field(description="Length in meters or 'N/A'")
    width_m: str = Field(description="Width in meters or 'N/A'")
    thickness_m: str = Field(default="N/A", description="Thickness in meters or 'N/A'")
    diameter_m: str = Field(default="N/A", description="Diameter in meters or 'N/A'")
    volume_m3: str = Field(description="Volume in cubic meters or 'N/A'")

class ComponentGeometryOutput(BaseModel):
    component_geometry: List[GeometryComponent]



component_geometry_agent = Agent(
    name="ComponentGeometryAgent",
    model="gemini-2.0-flash",
    description="Extracts geometric data of structural components and computes physical quantities such as volume or area using engineering formulas.",
    instruction="""
You will receive a PDF of a bridge General Arrangement Drawing (GAD).

Your task is to extract the geometry of structural components such as:
- Piers (P1, P2...)
- Abutments (A1, A2)
- Deck Slabs
- Girders
- Crash Barriers
- Cross Girders
- Wearing Coat
- Bearing Pedestal
- Approach Slabs
- Leveling Courses
- Dirt Wall

For each component, extract:
- Component name
- Shape (e.g., cylinder, rectangle, box, slab)
- Dimensions (height, length, width, diameter, thickness)
- Compute volume or area using appropriate formulas

**Volume Examples:**
- Cylinder: V = π × (D/2)^2 × H
- Slab/Block: V = L × W × T
- Area: A = L × W

Return result in **valid JSON only**. No extra explanation or text.

IMPORTANT: If any value is not found, use "N/A". Include all dimensions you find. Use engineering assumptions when needed.

Format:
{
  "component_geometry": [
    {
      "component": "Pier P1",
      "shape": "cylinder",
      "height_m": "6.5",
      "diameter_m": "1.2",
      "volume_m3": "7.36"
    }
  ]
}
""",
    output_schema=ComponentGeometryOutput,
    output_key="geometry_components",
)
