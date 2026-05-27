from ..models import EmissionRecord, Source, Tenant
from decimal import Decimal
from dateutil import parser as dateparser

# Example grid emission factor (kg CO2e per kWh) — placeholder, to be documented in SOURCES.md
GRID_EF = Decimal('0.233')


def parse_utility_csv(tenant: Tenant, source: Source, rows):
    created = []
    for row in rows:
        cons = row.get('consumption') or row.get('consumption_kwh') or row.get('cons')
        unit = row.get('unit') or 'kWh'
        start = row.get('start_date') or row.get('start')
        end = row.get('end_date') or row.get('end')

        try:
            amount = Decimal(str(cons)) if cons not in (None, '') else None
        except Exception:
            amount = None

        created_amount = None
        if amount is not None and unit and unit.lower() in ('kwh', 'kw*h', 'kilowatt-hour', 'kilowatt hours'):
            created_amount = (amount * GRID_EF).quantize(Decimal('0.000001'))

        rec = EmissionRecord.objects.create(
            tenant=tenant,
            source=source,
            source_row_id=row.get('meter_id') or None,
            category='electricity',
            scope=2,
            start_date=start or None,
            end_date=end or None,
            amount=amount,
            unit=unit,
            normalized_unit='kWh' if amount is not None else None,
            normalized_amount_kgco2e=created_amount,
            metadata=row,
        )
        created.append(rec.id)
    return created
