from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import List


class SeismicArrestorItem(BaseModel):
    component: str = Field(description="Component name (e.g., Transverse Seismic Stopper)")
    material: str = Field(description="Material type (e.g., Fe 410 Steel, Elastomeric)")
    quantity: str = Field(description="Number of units or 'N/A'")
    seismic_zone: str = Field(description="Seismic zone (e.g., Zone III) or 'N/A'")
    wind_zone: str = Field(description="Wind zone (e.g., Wind Zone V) or 'N/A'")
    design_codes: str = Field(description="Comma-separated list of relevant codes (e.g., IRC 6, IS 1893) or 'N/A'")
    location: str = Field(description="Application location (e.g., between Pier and Superstructure) or 'N/A'")


class SeismicArrestorsOutput(BaseModel):
    seismic_arrestors: List[SeismicArrestorItem]


seismic_arrestors_agent = Agent(
    name="SeismicArrestorsAgent",
    model="gemini-2.5-pro",
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

Return in valid JSON only. Use this format:
{
  "seismic_arrestors": [
    {
      "component": "Transverse Seismic Stopper",
      "material": "Fe 410 Steel",
      "quantity": "4",
      "seismic_zone": "Zone III",
      "wind_zone": "Zone V",
      "design_codes": "IRC 6, IRC 83 (Part-III)-2018",
      "location": "Between Pier P2 and deck"
    }
  ]
}

Use "N/A" where information is missing. If assumptions are made (e.g., inferred from drawing), briefly reflect that in the value.
""",
    output_schema=SeismicArrestorsOutput,
    output_key="seismic_arrestors"
)
