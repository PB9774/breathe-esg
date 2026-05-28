```md
# DECISIONS.md — Key Design Decisions

## 1. Why CSV Upload Instead of APIs?

I chose CSV uploads because that’s how most companies actually share data today. Utility providers and SAP systems usually don’t expose simple public APIs, and setting up integrations often requires client IT involvement. In practice, teams export reports manually and share flat files, so the system is designed around that workflow.

In the future, API-based ingestion can be added without changing the core data model.

---

## 2. Why SAP Flat Files Instead of IDoc/BAPI?

Flat CSV exports are the easiest and most realistic format for onboarding new clients. Every SAP system supports CSV exports, while IDocs and BAPIs require extra configuration, credentials, middleware, and technical setup.

The parser currently focuses only on fields needed for emissions calculation:
- quantity
- unit
- plant code
- material description

More complex SAP structures were intentionally skipped for simplicity.

**Known limitation:** some SAP exports may use non-English column headers, which would require a normalization layer in production.

---

## 3. Why These Emission Factors?

I used DEFRA 2023 emission factors because they are widely accepted, publicly available, and commonly used in corporate sustainability reporting.

Examples:
- Diesel: 2.68 kg CO2e/litre
- Electricity: 0.233 kg CO2e/kWh
- Flights: 0.255 kg CO2e/passenger-km

Using one trusted source keeps calculations consistent across categories.

---

## 4. Why No Authentication?

Authentication was skipped to keep the prototype focused on the core problem: data ingestion and emissions calculation.

A production-ready version would include proper login, permissions, and tenant isolation.

---

## 5. How Is Multi-Tenancy Handled?

For simplicity, each upload includes a `client_name` field. Records are filtered using this value during queries.

A full production system would use a dedicated `Client` model and stronger database-level isolation.

---

## 6. What Travel Data Is Supported?

The system handles trip-level records with distances already provided in kilometers.

Real travel platforms often provide airport codes but not calculated distances, which would require external lookup services. To keep the prototype lightweight, sample data already includes computed distances.

Hotel emissions and advanced travel calculations are outside the current scope.

---

