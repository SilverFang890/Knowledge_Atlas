# Contract: Search Pipeline

## Objective
Build a Python script that queries openly licensed image APIs and stores structured image metadata with provenance.

## Inputs
- space_types.json
- Pexels API
- API key from environment variable

## Processing
- Read room types
- Query API
- Extract image metadata
- Save structured JSON
- Respect rate limits

## Outputs
- search_results.json

## Success Conditions
- Every image contains:
  - url
  - thumbnail_url
  - source_name
  - source_page_url
  - license
  - space_type
- API keys are not hardcoded
- JSON validates
- Empty searches are logged