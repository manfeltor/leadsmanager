import requests
import json
from datetime import datetime, timedelta
import concurrent.futures
from django.core.management.base import BaseCommand
from kpisapp.models import SimpliRouteData, OBSERVATION_CHOICES
from leadsmanager.authvars import SRTOK

# API URL and headers
url = "https://api.simpliroute.com/v1/routes/visits/"
headers = {
    "authorization": f"Token {SRTOK}",
    "content-type": "application/json"
}

def get_status_by_uuid(uuid):
    for code, status in OBSERVATION_CHOICES:
        if code == uuid:
            return status
    return "Unknown UUID"


# Function to make the API request for a single date
def fetch_data_for_date(date_str):
    params = {"planned_date": date_str}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Invalid request for {date_str}: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Request error for {date_str}: {e}")
        return []

# Function to process data and save to the database
def process_data_for_month(start_date, end_date):
    # Generate list of dates for the current month
    date_list = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end_date - start_date).days + 1)]

    # Use ThreadPoolExecutor to fetch data in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_data_for_date, date_list))

    # Flatten the list of lists into a single list
    all_data_flattened = [item for sublist in results for item in sublist]

    if all_data_flattened:
        for delivery_data in all_data_flattened:
            # For each delivery, map the fields to the Django model
            delivery = SimpliRouteData(
                api_id=delivery_data.get("id"),
                tracking_id=delivery_data.get("tracking_id", ""),
                status=delivery_data.get("status", ""),
                title=delivery_data.get("title", ""),
                reference=delivery_data.get("reference", ""),
                planned_date=delivery_data.get("planned_date", None),
                programmed_date=delivery_data.get("programmed_date", None),
                created=delivery_data.get("created", None),
                visit_type=delivery_data.get("visit_type", ""),
                vehicle=delivery_data.get("vehicle", ""),
                checkout_observation=get_status_by_uuid(delivery_data.get('checkout_observation')),
                # checkout_observation=delivery_data.get("checkout_observation", "")
            )

            # Save the Delivery instance to the database
            delivery.save()

        print(f"Data for {start_date.strftime('%B %Y')} saved to the database.")
    else:
        print(f"No data retrieved for {start_date.strftime('%B %Y')}")

class Command(BaseCommand):
    help = 'Fetch delivery data and store it in the database'

    def handle(self, *args, **kwargs):
        # Define the start and end dates
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 9, 15)

        # Process data month by month
        current_date = start_date
        while current_date <= end_date:
            # Calculate the first day of the next month
            next_month = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
            # End of the current month is either the end_date or the last day of the current month
            last_day_of_month = min(next_month - timedelta(days=1), end_date)

            # Fetch and process data for the current month
            process_data_for_month(current_date, last_day_of_month)

            # Move to the next month
            current_date = next_month
