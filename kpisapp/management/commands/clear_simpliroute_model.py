from django.core.management.base import BaseCommand
from kpisapp.models import SimpliRouteData
from django.db import transaction

class Command(BaseCommand):
    help = 'Delete all data from SimpliRouteData table in batches'

    def handle(self, *args, **kwargs):
        confirm = input("Are you sure you want to delete all data from the SimpliRouteData table? (yes/no): ")
        if confirm.lower() == 'yes':
            batch_size = 1000  # Adjust the batch size according to your needs
            qs = SimpliRouteData.objects.all()
            total = qs.count()

            if total > 0:
                print(f"Deleting {total} records in batches of {batch_size}...")
                
                while total > 0:
                    with transaction.atomic():
                        # Fetch a batch of records to delete
                        ids_to_delete = list(qs.values_list('id', flat=True)[:batch_size])
                        
                        # Delete the batch
                        SimpliRouteData.objects.filter(id__in=ids_to_delete).delete()
                        total -= len(ids_to_delete)
                        print(f"Deleted {len(ids_to_delete)} records, {total} remaining.")
            
                self.stdout.write(self.style.SUCCESS('All data deleted successfully.'))
            else:
                self.stdout.write(self.style.ERROR('No records found to delete.'))

        else:
            self.stdout.write(self.style.ERROR('Operation cancelled.'))