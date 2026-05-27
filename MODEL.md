# MODEL.md

This document describes the data model for the prototype. It is intentionally concise and focused on the evaluation criteria: multi-tenancy, Scope 1/2/3, source-of-truth tracking, unit normalization, and audit trail.

Core entities
- Tenant: represents an enterprise customer. All records are tenant-scoped.
- Source: represents an ingestion source (SAP export, Utility CSV, Travel platform). Stores metadata about ingestion (type, original filename, imported_at, raw_payload reference).
- EmissionRecord: normalized row representing fuel/energy/travel activity with canonical columns:
  - tenant (FK)
  - source (FK)
  - source_row_id (string): original source's row ID if available
  - category (enum): 'fuel', 'procurement', 'electricity', 'travel'
  - scope (enum): 1/2/3
  - start_date, end_date
  - amount (decimal) and unit (string) — the original amount/unit
  - normalized_amount_kgco2e (decimal) — computed using emission factors
  - normalized_unit (string) — internal canonical unit (e.g., kWh, liters, passenger-km)
  - metadata (JSON): free-form source fields kept for audit
  - status (enum): 'pending_review', 'approved', 'rejected', 'locked'
  - created_at, updated_at
  - created_by, updated_by (nullable) — tracks analyst edits

Audit and provenance
- Each `EmissionRecord` stores `source` and `source_id` to trace origin. `Source` includes `ingested_at`, `filename`, and `raw_payload` (or pointer to raw storage) to provide a full audit trail.
- Edits and approvals update `updated_by` and `status`. Approvals also create `AuditLog` records to capture action, actor, and timestamp. Approved rows are considered locked for auditors.

Notes
- Unit normalization and emission factor application live in the ingestion adapters and are persisted as `normalized_amount_kgco2e` at ingestion time; raw values are retained in `amount`/`unit` and `metadata`.
- Source data raw payload is stored in `Source.raw_payload` to preserve the source-of-truth CSV content for audit.
