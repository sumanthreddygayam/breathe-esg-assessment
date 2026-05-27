from ..models import EmissionRecord, Source, Tenant
from decimal import Decimal
from dateutil import parser as dateparser


def parse_sap_csv(tenant: Tenant, source: Source, rows, category='fuel'):
    """Parse iterable of dict rows from a SAP-like CSV and create EmissionRecord rows."""
    created = []
    for row in rows:
        qty = row.get('quantity') or row.get('Quantity')
        uom = row.get('uom') or row.get('UOM') or row.get('units')
        posting = row.get('posting_date') or row.get('postingDate') or row.get('date')
        try:
            amount = Decimal(str(qty)) if qty not in (None, '') else None
        except Exception:
            amount = None

        try:
            start_date = dateparser.parse(posting).date() if posting else None
        except Exception:
            start_date = None

        # Normalize unit names
        if uom:
            u_lower = uom.lower()
            if 'gal' in u_lower:
                normalized_unit = 'gallon'
            elif 'l' == u_lower or 'litre' in u_lower or 'liter' in u_lower:
                normalized_unit = 'liter'
            else:
                normalized_unit = uom
        else:
            normalized_unit = None

        rec = EmissionRecord.objects.create(
            tenant=tenant,
            source=source,
            source_row_id=row.get('document_number') or row.get('document') or None,
            category=category,
            scope=None,
            start_date=start_date,
            end_date=start_date,
            amount=amount,
            unit=uom,
            normalized_unit=normalized_unit,
            metadata=row,
        )
        created.append(rec.id)
    return created
