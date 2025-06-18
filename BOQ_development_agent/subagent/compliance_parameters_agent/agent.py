from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import List


class ComplianceParameters(BaseModel):
    safety_standards: List[str] = Field(description="National or international safety standards referenced (e.g., IS 2911, IRC 78)")
    environmental_regulations: List[str] = Field(description="Environmental and geotechnical regulations (e.g., fill properties, emissions)")
    design_codes: List[str] = Field(description="Design codes (e.g., IS 456, IS 1786, IRC 6, IRC 83)")
    site_specific_notes: List[str] = Field(description="Site-specific conditions (e.g., Seismic zone, exposure class, wind zone)")
    quality_assurance: List[str] = Field(description="Quality protocols (e.g., testing, QA/QC, certification)")

class ComplianceParametersOutput(BaseModel):
    compliance_parameters: ComplianceParameters

compliance_parameters_agent = Agent(
    name="ComplianceParametersAgent",
    model="gemini-2.5-pro",
    description="Extracts compliance codes, safety standards, site-specific regulatory parameters, and quality protocols from bridge designs.",
    instruction="""
You will receive a bridge design PDF containing engineering drawings, general notes, and specifications.

Your task is to extract all compliance-related parameters and regulatory references, focusing on:

- Safety standards
- Environmental regulations
- Design and construction codes
- Site-specific compliance conditions (seismic, wind, soil, climate)
- Quality assurance and testing protocols

Identify and extract the following fields:
- safety_standards: National or international safety frameworks (e.g., IS 2911, IRC 78)
- environmental_regulations: Environmental mentions (e.g., emissions, earth fill properties)
- design_codes: Codes like IS 456, IS 1786, IRC 6, IRC 83
- site_specific_notes: Seismic zone, wind zone, exposure class, fill material instructions
- quality_assurance: Testing protocols (e.g., cube tests, slump tests, soil tests, certificates)

Return result in **valid JSON only**. No explanation or formatting.

Example:
{
  "compliance_parameters": {
    "safety_standards": ["IS 2911 (Part 4):2013", "IRC:78-2014"],
    "environmental_regulations": ["Earth fill must have C=0, φ>30°, γ=2T/m³"],
    "design_codes": ["IRC 6", "IS 456", "IS 383"],
    "site_specific_notes": ["Seismic Zone III", "Wind Zone V", "Exposure Class 'Severe'"],
    "quality_assurance": ["QA/QC Testing includes concrete cube testing, steel testing, and third-party certification"]
  }
}

If any value is not found, use an empty list []. Extract from:
- General Notes
- Drawing footnotes
- Compliance tables
- Project clauses
""",
    output_schema=ComplianceParametersOutput,
    output_key="compliance_parameters"
)
