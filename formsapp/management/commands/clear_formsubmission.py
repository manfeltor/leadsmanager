from django.core.management.base import BaseCommand
from formsapp.models import FormSubmission

class Command(BaseCommand):
    help = 'Delete all data from FormSubmission table'

    def handle(self, *args, **kwargs):
        confirm = input("Are you sure you want to delete all data from the FormSubmission table? (yes/no): ")
        if confirm.lower() == 'yes':
            FormSubmission.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('All data deleted successfully.'))
        else:
            self.stdout.write(self.style.ERROR('Operation cancelled.'))