from django.core.management.base import BaseCommand
from formsapp.models import FormSubmission
import requests
from requests.auth import HTTPBasicAuth
import logging
from leadsmanager.authvars import usrnm as a, passw as b, frmids as f
from .populate_formsubmission import normalize_submission

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def fetch_new_submissions():
    all_data = []
    for form_id in f:
        full_api_url = f'{base_api_url}{form_id}'
        data = get_form_submissions(full_api_url, a, b)
        if data:
            form_submissions = data.get('form_submissions', [])
            for submission in form_submissions:
                submission_id = submission.get('id')
                if not FormSubmission.objects.filter(submission_id=submission_id).exists():
                    processed_submission = normalize_submission(submission, form_id)
                    all_data.append(processed_submission)

    # Bulk create new FormSubmission entries
    form_submissions = [FormSubmission(**data) for data in all_data]
    FormSubmission.objects.bulk_create(form_submissions, ignore_conflicts=True)

class Command(BaseCommand):
    help = 'Fetch new form submissions and update the database'

    def handle(self, *args, **kwargs):
        fetch_new_submissions()
        self.stdout.write(self.style.SUCCESS('New submissions fetched successfully'))