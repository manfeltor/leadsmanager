from django.db import models

OBSERVATION_CHOICES = [
    ('1068d8b8-f939-46f7-8819-6ab130329ce9', 'Fuera de ruta asignada'),
    ('b068cd31-74c3-4f36-b60a-5f0a7b8837dd', 'Entregado'),
    ('e1b34560-430b-450d-a4df-55066d09172d', 'Colectado'),
    ('90fce0c5-4271-40f3-9f4f-71a6e3ee6e23', 'Ausente'),
    ('c689bc80-a295-458e-a858-1251afc1925c', 'Devolución Cliente'),
    ('1190098c-5ae2-467f-9ff8-ab839ac0555a', 'Domicilio Incorrecto'),
    ('4ae3ce34-2dc2-4a23-935b-93a7b0001875', 'Cancelado'),
    ('9e4619d2-240f-4efb-bc73-f91e9469cd91', 'Mercaderia no despachada'),
    ('d608375c-23cd-4ea3-bce8-25bfacc74ede', 'Zona peligrosa'),
    ('b77cf748-cd66-4c33-bdac-4b2ab0534b2b', 'Rechazado'),
    ('1a10310b-e710-4d66-8153-44ca9a88a8dc', 'No Colectado'),
    ('853eaa3c-c265-4c4d-96ef-95fe580114fe', 'Demoras Operativas'),
]

# Create your models here.
class SimpliRouteData(models.Model):
    # Django's internal ID (AutoField) will be used automatically as a primary key.
    api_id = models.BigIntegerField(unique=True)  # This stores the ID from the API
    tracking_id = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    reference = models.CharField(max_length=255, blank=True, null=True)
    planned_date = models.DateField()
    programmed_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField()
    visit_type = models.CharField(max_length=50, blank=True, null=True)
    vehicle = models.CharField(max_length=50, blank=True, null=True)
    checkout_observation = models.CharField(max_length=100, choices=OBSERVATION_CHOICES)


    def __str__(self):
        return f"Delivery {self.api_id} - {self.title}"