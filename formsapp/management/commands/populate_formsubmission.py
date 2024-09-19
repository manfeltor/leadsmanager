import requests
from requests.auth import HTTPBasicAuth
import json
from django.core.management.base import BaseCommand
from formsapp.models import FormSubmission
import logging
from ....leadsmanager.authvars import usrnm as a, passw as b, frmids as f

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve credentials and form IDs from environment variables
username = a
password = b
form_ids = f

# API base URL
base_api_url = 'https://intralog.com.ar/wp-json/custom/v1/form-submissions/'

def get_form_submissions(api_url, username, password):
    try:
        response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            logger.info(f"Successfully retrieved data from {api_url}")
            return response.json()
        else:
            logger.error(f"Failed to retrieve data from {api_url}: {response.status_code}")
            logger.error(f"Error message: {response.text}")
            return None
    except requests.RequestException as e:
        logger.error(f"Request failed for {api_url}: {e}")
        return None

def determine_avance_estado(servicio, form_id):
    if form_id != 7:
        if servicio == "Busco trabajo/ Ofrezco productos o servicios":
            return "▓", "negativo"
        else:
            return "⊕", "pendiente"
    else:
        return "⊕", "pendiente"

def normalize_submission(submission, form_id):
    servicio = submission.get('Me interesa el servicio' if form_id in [3, 4, 5] else 'Ubicación')
    avance, estado = determine_avance_estado(servicio, form_id)

    if form_id in [4, 5]:
        razon_social_key = "Razón Social"
        email_key = "Correo electrónico"
    else:
        if form_id == 3:
            email_key = "E-mail"
        else:
            email_key = "E-Mail"
        razon_social_key = "Razón social"

    processed = {
        "empresa": "INTRALOG" if form_id in [3, 4, 5] else "INTRAPAL",
        "submission_id": submission.get('id'),
        "fecha_creacion": submission.get('created_at'),
        "razon_social": submission.get(razon_social_key),
        "nombre_y_apellido": submission.get('Razón social' if form_id == 3 else 'Nombre y Apellido'),
        "telefono": submission.get('Teléfono' if form_id != 3 else 'Telefono'),
        "mail": submission.get(email_key),
        "mensaje": submission.get('Mensaje' if form_id in [3, 7] else 'Completa tu mensaje'),
        "servicio": servicio,
        "origen": "Web",
        "sub_origen": "Signos",
        "avance": avance,
        "estado": estado,
        "form_id": form_id,
        "data": submission,  # Store the raw JSON data
        "assigned_user_id": 3 if form_id in [3, 4, 5] else 2
    }
    return processed

class Command(BaseCommand):
    help = 'Import form submissions from JSON data'

    def handle(self, *args, **kwargs):
        all_data = []

        for form_id in form_ids:
            full_api_url = f'{base_api_url}{form_id}'
            data = get_form_submissions(full_api_url, username, password)
            if data:
                form_submissions = data.get('form_submissions', [])
                for submission in form_submissions:
                    processed_submission = normalize_submission(submission, form_id)
                    all_data.append(processed_submission)

        # Bulk create FormSubmission entries
        form_submissions = [FormSubmission(**data) for data in all_data]
        FormSubmission.objects.bulk_create(form_submissions, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
