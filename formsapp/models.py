from django.db import models

# Create your models here.
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
    estado = models.CharField(max_length=50)
    form_id = models.IntegerField()
    submission_id = models.IntegerField(unique=True)
    data = models.JSONField()  # Store the raw JSON data

    def __str__(self):
        return f"Form {self.form_id} Submission {self.submission_id}"