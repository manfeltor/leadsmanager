import requests
import logging
from requests.auth import HTTPBasicAuth
from celery import shared_task
from django.utils import timezone
from formsapp.models import FormSubmission, CustomUser  # Import models
from leadsmanager.authvars import usrnm as a, passw as b, frmids as f
from formsapp.management.commands.populate_formsubmission import determine_avance_estado

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base API URL
base_api_url = 'https://intralog.com.ar/wp-json/custom/v1/form-submissions/'

# Function to get form submissions from API
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

# Function to normalize a submission
def normalize_submission(submission, form_id):
    servicio = submission.get('Me interesa el servicio' if form_id in [3, 4, 5] else 'Ubicación')
    avance, estado = determine_avance_estado(servicio, form_id)

    razon_social_key = "Razón Social" if form_id in [4, 5] else "Razón social"
    email_key = "Correo electrónico" if form_id in [4, 5] else "E-Mail"

    processed = {
        "empresa": "INTRALOG" if form_id in [3, 4, 5] else "INTRAPAL",
        "submission_id": submission.get('id'),
        "fecha_creacion": submission.get('created_at'),
        "razon_social": submission.get(razon_social_key),
        "nombre_y_apellido": submission.get('Nombre y Apellido'),
        "telefono": submission.get('Teléfono'),
        "mail": submission.get(email_key),
        "mensaje": submission.get('Mensaje'),
        "servicio": servicio,
        "origen": "Web",
        "sub_origen": "Signos",
        "avance": avance,
        "estado": estado,
        "form_id": form_id,
        "data": submission,  # Store the raw JSON data
        # Use hardcoded values for 'assigned_user' and 'campaign'
    }
    return processed

initial_user = 6
current_campaign = None

@shared_task
def fetch_new_submissions():
    # Get the hardcoded user to be assigned to new submissions
    try:
        assigned_user = CustomUser.objects.get(pk=initial_user)  # Replace with the desired user ID
    except CustomUser.DoesNotExist:
        logger.error("User with ID 1 does not exist.")
        return

    # Prepare to store the new form submissions
    all_data = []
    
    for form_id in f:
        full_api_url = f'{base_api_url}{form_id}'
        data = get_form_submissions(full_api_url, a, b)
        
        if data:
            form_submissions = data.get('form_submissions', [])
            for submission in form_submissions:
                submission_id = submission.get('id')
                
                # Only process new submissions
                if not FormSubmission.objects.filter(submission_id=submission_id).exists():
                    processed_submission = normalize_submission(submission, form_id)
                    
                    # Convert fecha_creacion to aware datetime
                    fecha_creacion_str = processed_submission['fecha_creacion']
                    processed_submission['fecha_creacion'] = timezone.make_aware(
                        timezone.datetime.strptime(fecha_creacion_str, '%Y-%m-%d %H:%M:%S'), 
                        timezone.get_current_timezone()
                    )

                    # Add hardcoded 'assigned_user' and 'campaign' (None for now)
                    processed_submission['assigned_user'] = assigned_user
                    processed_submission['campaign'] = current_campaign
                    
                    # Create a FormSubmission object
                    form_submission_instance = FormSubmission(**processed_submission)
                    all_data.append(form_submission_instance)

    # Bulk create the form submissions in the database
    FormSubmission.objects.bulk_create(all_data, ignore_conflicts=True)
    logger.info('New submissions fetched and saved successfully.')