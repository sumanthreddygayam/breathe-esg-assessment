from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import csv

from ingest.models import Tenant, Source
from ingest.parsers import sap_parser, utility_parser, travel_parser


class Command(BaseCommand):
    help = 'Load sample CSVs into the database for demo/testing.'

    def handle(self, *args, **options):
        base = Path(settings.BASE_DIR).parent  # repo root
        sample_dir = base / 'sample_data'

        tenant, _ = Tenant.objects.get_or_create(name='Demo Tenant')

        # SAP fuel
        sap_fuel_path = sample_dir / 'sap_fuel.csv'
        if sap_fuel_path.exists():
            with sap_fuel_path.open(encoding='utf-8') as f:
                reader = csv.DictReader(f)
                source = Source.objects.create(tenant=tenant, source_type='sap_fuel', filename=str(sap_fuel_path))
                created = sap_parser.parse_sap_csv(tenant, source, reader, category='fuel')
                self.stdout.write(f'Created {len(created)} SAP fuel records')

        sap_proc_path = sample_dir / 'sap_procurement.csv'
        if sap_proc_path.exists():
            with sap_proc_path.open(encoding='utf-8') as f:
                reader = csv.DictReader(f)
                source = Source.objects.create(tenant=tenant, source_type='sap_procurement', filename=str(sap_proc_path))
                created = sap_parser.parse_sap_csv(tenant, source, reader, category='procurement')
                self.stdout.write(f'Created {len(created)} SAP procurement records')

        util_path = sample_dir / 'utility_electricity.csv'
        if util_path.exists():
            with util_path.open(encoding='utf-8') as f:
                reader = csv.DictReader(f)
                source = Source.objects.create(tenant=tenant, source_type='utility_electricity', filename=str(util_path))
                created = utility_parser.parse_utility_csv(tenant, source, reader)
                self.stdout.write(f'Created {len(created)} utility records')

        travel_path = sample_dir / 'travel_export.csv'
        if travel_path.exists():
            with travel_path.open(encoding='utf-8') as f:
                reader = csv.DictReader(f)
                source = Source.objects.create(tenant=tenant, source_type='travel_export', filename=str(travel_path))
                created = travel_parser.parse_travel_csv(tenant, source, reader)
                self.stdout.write(f'Created {len(created)} travel records')

        self.stdout.write(self.style.SUCCESS('Sample data load complete'))
