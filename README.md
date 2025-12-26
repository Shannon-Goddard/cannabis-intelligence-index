# 🌿 Cannabis Intelligence Index (CII)
### The Industrial-Scale Medallion Architecture for Global Cultivar Data

**Project Status:** Production Phase (15,695 strains processing)

**Infrastructure:** AWS (Security) + Google Cloud (Compute)

**Methodology:** Tri-Model AI Synthesis (Gemini 2.5 + Amazon Q)

The **Cannabis Intelligence Index** is the production-grade successor to the Cannabis Intelligence Database. It utilizes a specialized **Medallion Architecture** to bridge the gap between fragmented commercial breeder data and standardized botanical science.




```
cannabis-intelligence-index/
├── .github/                   # GitHub-specific configurations
│   └── workflows/             # (Optional) For automated testing
├── config/                    # Configuration templates (No real keys!)
│   ├── gcp_config_sample.yaml
│   └── aws_config_sample.yaml
├── docs/                      # Extensive documentation
│   ├── architecture/          # Diagrams and "Medallion" explanations
│   ├── api/                   # API Documentation (Amazon Q's future input)
│   ├── decision_log.md        # The Decision Log we drafted
│   └── data_dictionary.md     # The Data Dictionary file
├── src/                       # The "Proof of Work" (The Code)
│   ├── ingestion/             # Scripts that handled the breeder sites
│   ├── processing/            # Gemini's batch generation scripts
│   ├── security/              # AWS Secrets Manager integration logic
│   └── utils/                 # HTML sanitizers and cleaners
├── samples/                   # "Teaser" data for Gumroad buyers
│   ├── sample_bronze.json     # 5-10 rows of raw extraction
│   └── sample_gold.csv        # 5-10 rows of standardized data
├── .gitignore                 # CRITICAL: Prevents data/keys from leaking
├── LICENSE_CODE               # MIT License for your scripts
├── LICENSE_DATA.md            # The Custom Commercial License we drafted
├── PROJECT_SUMMARY.md         # The DOI Summary (Data Architect + Systems Engineer)
└── README.md                  # The Main "Handshake" Page
```