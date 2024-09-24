import os
import pandas as pd
from django.core.management.base import BaseCommand
from kpisapp.models import OmsData
from datetime import datetime
from django.utils import timezone

# Helper function to safely parse a date from the Excel file
def parse_date(date_value):
    if pd.isna(date_value):
        return None
    try:
        # Convert to a pandas datetime object
        parsed_date = pd.to_datetime(date_value)

        # Check if the date is naive (doesn't have timezone info)
        if parsed_date.tzinfo is None:
            # Make it timezone-aware using Django's timezone settings
            return timezone.make_aware(parsed_date)
        return parsed_date
    except ValueError:
        return None

class Command(BaseCommand):
    help = 'Load orders from multiple Excel files in a folder into the Order model'

    def handle(self, *args, **kwargs):
        # Define the folder where the Excel files are located
        folder_path = r"C:\Users\manfe\Downloads\tms_compi"  # Change this to your folder path

        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                file_path = os.path.join(folder_path, filename)
                print(f"Processing {file_path}...")

                # Read the Excel file into a pandas DataFrame
                df = pd.read_excel(file_path)

                # Iterate over the DataFrame rows and create Order objects
                for _, row in df.iterrows():
                    try:
                        order = OmsData(
                            pedido=row['pedido'],
                            flujo=row['flujo'],
                            seller=row['seller'],
                            sucCodigo=row['sucCodigo'],
                            sucursal=row['sucursal'],
                            estadoPedido=row['estadoPedido'],
                            fechaCreacion=parse_date(row['fechaCreacion']),
                            fechaRecepcion=parse_date(row['fechaRecepcion']),
                            fechaDespacho=parse_date(row['fechaDespacho']),
                            fechaEntrega=parse_date(row['fechaEntrega']),
                            lpn=row['lpn'],
                            estadoLpn=row['estadoLpn'],
                            zona=row['zona'],
                            transporte=row.get('transporte', ''),  # Handle optional fields
                            trackingColecta=row.get('trackingColecta', ''),
                            trackingDistribucion=row.get('trackingDistribucion', ''),
                            trackingTransporte=row.get('trackingTransporte', ''),
                            tipo=row.get('tipo', ''),
                            codigoPostal=row['codigoPostal'],
                            tte=row.get('tte', ''),
                            tteSucursalDistribucion=row.get('tteSucursalDistribucion', ''),
                            tiendaEntrega=row.get('tiendaEntrega', ''),
                        )
                        order.save()
                        # print(f"Saved order {order.pedido}")
                    except Exception as e:
                        print(f"Error saving order from row: {row['pedido']}. Error: {e}")

        print("All files processed.")