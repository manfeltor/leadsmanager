import openpyxl
from django.core.management.base import BaseCommand
from formsapp.models import FormSubmission
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = "Export FormSubmission data to an Excel file"

    def handle(self, *args, **kwargs):
        # Query all FormSubmission objects
        submissions = FormSubmission.objects.all()

        # Create a new Excel workbook and sheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Form Submissions"

        # Define the header row
        headers = [
            "ID", "Fecha Creación", "Razon Social", "Nombre y Apellido",
            "Estado", "Mensaje", "Email", "Teléfono", "Origen", "Sub Origen", 
            "Avance", "Usuario Asignado"
        ]
        ws.append(headers)

        # Iterate through FormSubmission objects and write rows
        for submission in submissions:
            row = [
                submission.id,
                submission.fecha_creacion.strftime('%Y-%m-%d'),
                submission.razon_social,
                submission.nombre_y_apellido,
                submission.estado,
                submission.mensaje,
                submission.mail,
                submission.telefono,
                submission.origen,
                submission.sub_origen,
                submission.avance,
                submission.assigned_user.username if submission.assigned_user else "N/A"
            ]
            ws.append(row)

        # Define a filename with the current timestamp
        current_time = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f'Form_Submissions_{current_time}.xlsx'

        # Save the workbook to an Excel file
        wb.save(filename)

        # Output a success message
        self.stdout.write(self.style.SUCCESS(f"Data exported successfully to {filename}"))