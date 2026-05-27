# SOURCES.md

Research notes and sample data rationale for each source.

## SAP

- Real-world formats: SAP exports are often produced from SAP GUI reports, SE16/SE16N table extracts, or SAP BW/BI exports. Larger implementations also use IDoc/BAPI/OData, but CSV remains the easiest onboarding shape for a prototype.
- Prototype choice: CSV exports of fuel movements and procurement lines. This captures the most common early ingestion path when a sustainability team hands over a file.
- Realism in sample data: plant codes are opaque (`PLANT_A`, `PLANT_B`, `PLANT_C`), units are mixed (`l`, `litre`, `gal`, `liters`), and posting dates are formatted both `YYYY-MM-DD` and `DD.MM.YYYY`.
- What breaks in production: true SAP IDocs or API payloads, missing SAP plant/plant-code lookup tables, or files that are not UTF-8 encoded.

## Utility electricity CSV

- Real-world formats: utilities commonly provide portal CSV exports with meter readings and billed consumption. These are used by facilities teams when a direct API is not available.
- Prototype choice: a CSV with `meter_id`, `start_date`, `end_date`, `consumption`, `unit`, and `billing_amount`.
- Realism in sample data: billing periods do not align neatly to calendar months, and periods may have different start/end boundaries.
- What breaks in production: time-of-use tariffs, demand charge structures, and aggregated or nested meter detail.

## Corporate travel

- Real-world formats: Concur and Navan both support CSV exports of trip segments, which is a more realistic onboarding interface than requiring direct API connectivity.
- Prototype choice: segment-level CSV with `trip_id`, `employee_id`, `segment_type`, `origin`, `destination`, `distance_km`, `start_date`, and `end_date`.
- Realism in sample data: `flight` and `car` segments are mixed, some rows have explicit distance, and one hotel segment is included to demonstrate how travel categories differ.
- What breaks in production: API-only itinerary exports, multi-leg airport distance resolution, and cases where only spend is provided without distance or activity detail.

## Sample files
- `sample_data/sap_fuel.csv`: SAP fuel movements with mixed units and date formats.
- `sample_data/sap_procurement.csv`: procurement rows with quantities and UoM.
- `sample_data/utility_electricity.csv`: electricity meter readings and billing periods.
- `sample_data/travel_export.csv`: travel segments covering flights, car travel, and hotels.

## Why these samples?
- They demonstrate realistic ingestion challenges: mixed units, locale-specific dates, billing periods that do not align to calendar months, and incomplete travel distance data.
- They also reflect the source-of-truth mindset: raw payload is preserved and normalized records keep original metadata for auditor review.

