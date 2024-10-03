import pandas as pd
from django.core.management.base import BaseCommand
from formsapp.models import FormSubmission

class Command(BaseCommand):
    help = 'Update the estado field based on an XLSX file matching on mail or razon_social'

    def add_arguments(self, parser):
        parser.add_argument('xlsx_path', type=str, help='Path to the XLSX file')

    def handle(self, *args, **kwargs):
        xlsx_path = kwargs['xlsx_path']

        # Load the data from the XLSX file
        df = pd.read_excel(xlsx_path)

        # Ensure the required columns exist in the XLSX file
        if 'mail' not in df.columns or 'estado' not in df.columns or 'cliente' not in df.columns:
            self.stdout.write(self.style.ERROR("The XLSX file must contain 'mail', 'estado', and 'cliente' columns."))
            return

        # Iterate over FormSubmission objects to update them
        updated_count = 0
        for submission in FormSubmission.objects.exclude(estado='negativo'):
            # Step 1: Try to match by mail
            matched_row = df[df['mail'] == submission.mail]

            # Step 2: If no match by mail, try matching by razon_social
            if matched_row.empty:
                matched_row = df[df['cliente'] == submission.razon_social]

            # Step 3: If no match is found, set estado to 'noDefinido'
            if matched_row.empty:
                submission.estado = submission.estado
            else:
                # Update estado with the value from the matched row
                submission.estado = matched_row['estado'].values[0]

            # Save the updated submission object
            submission.save()
            updated_count += 1

        self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} FormSubmission entries."))