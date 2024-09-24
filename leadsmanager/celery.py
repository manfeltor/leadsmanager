from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leadsmanager.settings')

app = Celery('leadsmanager')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Import the task only inside the function to avoid premature app loading
#     from formsapp.tasks.update_forms import fetch_new_submissions

#     # Add periodic task to Celery's schedule
#     sender.add_periodic_task(
#         fetch_new_submissions.s(),
#     )