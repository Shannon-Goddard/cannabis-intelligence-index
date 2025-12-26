## 🏗️ System Architecture: Medallion & Tri-Model Synthesis
The **Cannabis Intelligence Index (CII)** utilizes a modular, multi-cloud architecture designed for scientific auditability and enterprise-grade security.
### 1. The Medallion Data Pipeline
We follow the Medallion Architecture to incrementally refine raw, unstructured breeder data into a standardized, analytics-ready "Gold" product.
#### 🥉 Bronze Layer (Source of Truth):
- **State:** Raw Ingestion.
- **Logic:** Verbatim extraction of data from 15,695 seed bank sources.
- **Purpose:** Ensures a "Zero-Interpretation" audit trail. If a standardized value is ever questioned, the original source string is preserved here for verification.
#### 🥇 Gold Layer (Standardized Index):
- **State:** Analytics-Ready.
- **Logic:** Normalization of subjective descriptors and disparate units (e.g., converting "8 weeks" to "56 days" or "Tall" to standardized "cm" ranges).
- **Purpose:** Provides a machine-readable dataset optimized for API consumption and scientific comparative analysis.
### 2. Tri-Model Orchestration
To ensure unbiased data and secure infrastructure, the project is governed by three distinct agents:
| Agent         | Domain  | Role | 
|--------------------|--------|-----------|
|Human Mediator|Oversight|Final decision-making on data logic and strategic project direction.|
|Gemini 2.5|Data Architect|Botanical reasoning, HTML sanitization, and Bronze-to-Gold synthesis.|
|Amazon Q|Systems Engineer|Secure cloud integration, AWS Secrets Manager orchestration, and API documentation.

### 3. Infrastructure & Security
- **Cloud Hybridization:** We utilize AWS for security and identity management while leveraging Google Cloud (Vertex AI) for high-throughput batch processing.
- **Secrets Management:** Authentication keys are never stored locally; they are managed and rotated via **AWS Secrets Manager**, ensuring the production pipeline is secured against credential leaks.
- **Validation Framework:** Automated "Sanity Scripts" run during the transition from Bronze to Gold to identify and flag statistical outliers or contradictory breeder claims.