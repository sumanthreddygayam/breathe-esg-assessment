# TRADEOFFS.md

Three deliberate omissions and why:

1. Real-time API connectors for each vendor: building robust API integrations would consume most of the time; file uploads cover the common onboarding path and are more realistic for early onboarding.
2. Full enterprise RBAC and SSO: prototype uses DRF token-based auth and a demo analyst user for speed; production should use SSO and role-based access control.
3. Full source validation / schema discovery: the app accepts CSVs with heuristic field matching rather than a strict contract, because handling every enterprise variant would require much more engineering than the prototype window allows.
