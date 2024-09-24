from django.core.management.base import BaseCommand
from kpisapp.models import OmsData, SimpliRouteData, OrderTrackingRelation

class Command(BaseCommand):
    help = 'Populate OrderTrackingRelation with left join from OmsData to SimpliRouteData'

    def handle(self, *args, **kwargs):
        # Query all OmsData entries that have a trackingTransporte
        oms_data_entries = OmsData.objects.exclude(trackingDistribucion__isnull=True).exclude(trackingDistribucion__exact='')

        # Iterate over each OmsData entry and try to find a corresponding SimpliRouteData
        for oms_data in oms_data_entries:
            try:
                simpli_route_data = SimpliRouteData.objects.get(tracking_id=oms_data.trackingDistribucion)
                
                # If a matching SimpliRouteData is found, create the relation
                relation, created = OrderTrackingRelation.objects.get_or_create(
                    oms_data=oms_data,
                    simpli_route_data=simpli_route_data
                )

                # if created:
                    # self.stdout.write(self.style.SUCCESS(f"Created relation for OmsData.pedido: {oms_data.pedido}"))

            except SimpliRouteData.DoesNotExist:
                # Handle case where no matching SimpliRouteData entry is found
                self.stdout.write(self.style.WARNING(f"No matching SimpliRouteData for OmsData.pedido: {oms_data.pedido}"))

        self.stdout.write(self.style.SUCCESS("OrderTrackingRelation population completed"))