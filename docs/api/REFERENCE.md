## 📡 API Reference & Schema Definitions
The **Cannabis Intelligence Index (CII**) is delivered as a standardized JSON-L (JSON Lines) dataset. This format is optimized for high-performance ingestion into vector databases (for AI apps) or relational SQL tables.
### 1. The "Gold" Object Schema
Each entry in the index follows this strictly typed structure.
```
{
  "index_id": "CII-7890-X",
  "strain_name": "Future #1",
  "botanical_profile": {
    "type": "Hybrid",
    "genetics": ["Gorilla Glue #4", "Starfighter"],
    "standardized_metrics": {
      "thc_pct_max": 37.0,
      "flower_days_avg": 63,
      "height_cm_avg": 140
    }
  },
  "metadata": {
    "confidence_score": 5,
    "last_updated": "2025-12-25",
    "bronze_audit_source": "https://source-link.com/cultivar-page",
    "bronze_raw_string": "Flowering time is approx 9 weeks with THC up to 37%."
  }
}
```
### 2. Field Definitions
| Key        | Type  | Description | 
|--------------------|--------|-----------|
|index_id|UUID|Unique identifier within the CII ecosystem.|
|thc_pct_max|Float|The ceiling THC value found in breeder reports.|
|flower_days_avg|Integer|"Standardized duration (e.g., ""9 weeks"" → 63)."|
|confidence_score|1-5|5 = High (Verified by multiple agents); 1 = Low (Incomplete source).|
|bronze_raw_string|String|The Audit Trail. Verbatim text used to generate the Gold metrics.|
### 3. Implementation Example (Python)
If a user wants to filter your "Gold Layer" for high-potency strains:
```
Python import json

# Load the Gold Layer
with open('cii_gold_layer.jsonl', 'r') as f:
    high_potency = [json.loads(line) for line in f  
                    if json.loads(line)['botanical_profile']['standardized_metrics']['thc_pct_max'] > 30.0]

print(f"Found {len(high_potency)} elite cultivars.")
```
