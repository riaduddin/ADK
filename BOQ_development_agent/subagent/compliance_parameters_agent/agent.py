from google.adk.agents import Agent


compliance_parameters_agent = Agent(
    name="ComplianceParametersAgent",
    model="gemini-2.0-flash",
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

Return output in the following format:
```json
{
  "compliance_parameters": {
    "safety_standards": ["IS 2911 (Part 4):2013", "IRC:78-2014"],
    "environmental_regulations": ["Earth fill must have C=0, φ>30°, γ=2T/m³"],
    "design_codes": ["IRC 6", "IS 456", "IS 383"],
    "site_specific_notes": ["Seismic Zone III", "Wind Zone V", "Exposure Class 'Severe'"],
    "quality_assurance": ["QA/QC Testing includes concrete cube testing, steel testing, and third-party certification"]
  }
}
Be concise but complete. If a section is missing, use "N/A" or return an empty list.

Look for information in:

General Notes

Footnotes on drawings

Compliance tables

Project-specific clauses
""",
    output_key="compliance_parameters"
        )