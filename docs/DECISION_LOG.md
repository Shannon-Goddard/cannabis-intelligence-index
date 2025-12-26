## 📓 Architectural Decision Log
### Decision 1: Tri-Model Mediation (2025-12-25)
**Context:** To avoid "Model Bias" and ensure industrial-grade security. **Action:** Decided to use Gemini 3 Flash as the **Botanical Data Architect** and Amazon Q as the **Cloud Systems Engineer**. Shannon Goddard acted as the **Human Mediator** to resolve logic conflicts. **Outcome:** Created a balanced system where data accuracy is prioritized by one AI and infrastructure security by the other.

### Decision 2: The "Zero-Interpretation" Bronze Layer
**Context:** AI "hallucinations" are a risk in scientific data. **Action:** Mandated a two-tier Medallion Architecture. The Bronze layer stores verbatim strings (e.g., "approx 60 days") while the Gold layer standardizes them. **Outcome:** Full scientific auditability. Any user can verify the "Gold" data by checking the "Bronze" source string.

### Decision 3: Cross-Cloud Security Strategy
**Context:** Managing credentials for 15,000+ automated requests. **Action:** Stored Google Service Account keys in **AWS Secrets Manager** rather than local .env files. **Outcome:** Enterprise-grade security. Credentials are never "at rest" on the local machine during the batch run.