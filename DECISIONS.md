# DECISIONS.md

This document will record choices about source formats, ingestion mechanisms, and scope limits. It will be completed as the prototype is implemented. Initial decisions:

- SAP: chosen a pragmatic CSV export path for fuel movements (`sap_fuel.csv`) and procurement orders (`sap_procurement.csv`). This mirrors real SAP onboarding where customers export ad hoc reports from SAP GUI/SE16 or SAP BI.
- Utility: modeled the CSV portal export path with meter readings and billing periods, consistent with facilities team exports rather than direct API integration.
- Travel: modeled corporate travel exports as a CSV trip segment file, which is a common onboarding format for Concur/Navan. The prototype accepts `flight`, `hotel`, and `car` travel segments.

Subsets handled
- SAP only handles fuel and procurement rows, not full IDocs, BAPIs, or SAP OData. It normalizes mixed units and date formats.
- Utility only handles electricity meter readings in kWh and does not model time-of-use tariff pricing or demand charges.
- Travel only handles single-segment distances and simple per-mode emission factors; it does not resolve airport-code distances automatically.

Questions for PM
- Should we use internal company emission factors or published GHG Protocol factors for Scope 1/2/3?
- Which tenancy model is preferred: one tenant per company or one tenant per client with multiple facilities?
- Should approvals be captured as a separate audit entity for later sign-off tracking? (Yes, this prototype does.)
