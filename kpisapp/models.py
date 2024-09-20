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
    tracking_id = models.CharField(max_length=50, unique=True)
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
    

class OmsData(models.Model):
    pedido = models.CharField(max_length=50)
    flujo = models.CharField(max_length=5)
    seller = models.CharField(max_length=50)
    sucCodigo = models.CharField(max_length=50)
    sucursal = models.CharField(max_length=10)
    estadoPedido = models.CharField(max_length=50)
    fechaCreacion = models.DateTimeField()
    fechaRecepcion = models.DateTimeField(null=True, blank=True)
    fechaDespacho = models.DateTimeField(null=True, blank=True)
    fechaEntrega = models.DateTimeField(null=True, blank=True)
    lpn = models.CharField(max_length=30)
    estadoLpn = models.CharField(max_length=50)
    zona = models.CharField(max_length=50)
    transporte = models.CharField(max_length=100, null=True, blank=True)
    trackingColecta = models.CharField(max_length=255, null=True, blank=True)
    trackingDistribucion = models.CharField(max_length=255, null=True, blank=True)
    trackingTransporte = models.CharField(max_length=255, null=True, blank=True)
    fechaRecepcion = models.DateTimeField(null=True, blank=True)
    tipo = models.CharField(max_length=50, null=True, blank=True)
    codigoPostal = models.CharField(max_length=20)
    tte = models.CharField(max_length=100, null=True, blank=True)
    tteSucursalDistribucion = models.CharField(max_length=100, null=True, blank=True)
    tiendaEntrega = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Order {self.pedido}"
    

class OrderTrackingRelation(models.Model):
    oms_data = models.ForeignKey('OmsData', on_delete=models.SET_NULL, null=True, blank=True)
    simpli_route_data = models.ForeignKey('SimpliRouteData', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"OrderTrackingRelation({self.oms_data.pedido if self.oms_data else 'No OmsData'}, {self.simpli_route_data.tracking_id if self.simpli_route_data else 'No SimpliRouteData'})"