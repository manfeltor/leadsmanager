from django.db import models
from usersapp.models import CustomUser
from django.contrib.auth import get_user_model

ESTADO_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('asignado', 'Asignado'),
    ('contactado', 'Contactado'),
    ('faltaCotizar', 'Falta cotizar'),
    ('cotizado', 'Cotizado'),
    ('interesadoAvanzar', 'Interesados en avanzar'),
    ('gestionExitosa', 'Gestion exitosa'),
    ('pospuesto', 'pospuesto'),
    ('noAvanzo', 'No avanzo'),
    ('noViable', 'No viable'),
    ('nuevoCliente', 'Nuevo cliente'),
    ('negativo', 'Negativo'),
    ('noDefinido', 'No definido'),
]

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class FormSubmission(models.Model):

    empresa = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField()
    razon_social = models.CharField(max_length=255, blank=True, null=True)
    nombre_y_apellido = models.CharField(max_length=255, blank=True, null=True)
    servicio = models.CharField(max_length=255, blank=True, null=True)
    mail = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    origen = models.CharField(max_length=255)
    sub_origen = models.CharField(max_length=255)
    mensaje = models.TextField(blank=True, null=True)
    avance = models.CharField(max_length=50)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    form_id = models.IntegerField()
    submission_id = models.IntegerField(unique=True)
    data = models.JSONField()  # Store the raw JSON data
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_user')
    management_message = models.TextField(null=True, blank=True)
    campaign = models.ForeignKey('Campaign', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user from kwargs

        if self.pk:  # If this is an update
            old_instance = FormSubmission.objects.get(pk=self.pk)
            if old_instance.estado != self.estado:
                LeadHistory.objects.create(
                    form_submission=self,
                    previous_status=old_instance.estado,
                    new_status=self.estado,
                    updated_by=user
                )
        else:  # If this is a new submission
            LeadHistory.objects.create(
                form_submission=self,
                previous_status=None,
                new_status=self.estado,
                updated_by=user
            )

        super(FormSubmission, self).save(*args, **kwargs)


class LeadHistory(models.Model):
    
    form_submission = models.ForeignKey('FormSubmission', on_delete=models.CASCADE, related_name='history')
    previous_status = models.CharField(max_length=50, choices=ESTADO_CHOICES, blank=True, null=True)
    new_status = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    updated_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead {self.form_submission.submission_id} - {self.new_status} by {self.updated_by}"
