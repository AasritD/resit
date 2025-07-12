# GDPR, Ethics & Data Protection

This document summarises how our **Advanced AI** pipeline addresses UK GDPR and the ICO’s AI & Data Protection Toolkit requirements.  

## 1. Reference

We follow the ICO’s **AI & Data Protection Toolkit** guidance:  
https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/ai-and-data-protection-risk-toolkit/ :contentReference[oaicite:3]{index=3}

## 2. Data Minimisation & Anonymisation

- **Dropped PII**: All direct identifiers (e.g. names, addresses) were removed before ingestion.  
- **Field renaming**: Sensitive column `Driver Name` was omitted; `Driver Age` was binned into 5-year ranges (`DriverAge`) to reduce re-identification risk.  
- **Limited scope**: Only features with clear relevance to settlement prediction were retained; unused free-text or image fields were excluded.

## 3. Lawful Basis & Transparency

- **Purpose limitation**: Data is used solely to predict “settlement value” to improve claims processing.  
- **Transparency**: User documentation (README + this file) clearly states what data is processed and why, ensuring auditability.

## 4. Fairness, Accountability & Trust

- **Protected attributes**: We explicitly include **Age** and **Gender** only for subgroup fairness analysis, not for downstream decisioning.  
- **Fairness checks**: We compute MAPE by Age×Gender subgroup and compare performance to detect bias :contentReference[oaicite:4]{index=4}.  
- **Hybrid models**: If significant subgroup disparities appear (MAPE gap > 5 %), we plan hybrid sub-model pipelines to equalise accuracy.

## 5. Explainability & User Control

- **Global explainability**: SHAP summary plots surface which features most drive predictions.  
- **Local explainability**: A `predict_and_explain()` helper provides per-record waterfall charts so case-handlers see exactly how each feature contributed.  
- **Human-in-the-loop**: End-users can override predictions; all overrides are logged for retraining and audit.

## 6. Ongoing Monitoring & Data Retention

- **Logging**: Every prediction, explanation, and override is logged (no PII) to enable model retraining and drift detection.  
- **Retention policy**: Logs older than 90 days are aggregated and anonymised before long-term storage, in line with our Data Retention Schedule.

## 7. Residual Risks & Mitigations

| Risk                                                      | Mitigation                                  |
|-----------------------------------------------------------|---------------------------------------------|
| Small subgroup sizes → unreliable MAPE estimates          | Aggregate adjacent age bins if < 30 samples |
| Potential re-identification via feature combinations      | Limit storage of raw feature vectors; only store preprocessed arrays |
| Unintended use of “protected” attributes in decision-making | Documentation + access control on subgroup analyses |
