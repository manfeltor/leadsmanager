from django import forms
from .models import FormSubmission, ESTADO_CHOICES
from usersapp.models import CustomUser

#TODO push nuevo form carga manual subm .1, sobre edit manual form .1

class FormSubmissionEditForm(forms.ModelForm):
    assigned_user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role='employee'), required=False)
    
    SERVICIO_CHOICES = [
    ('', '--------'),
    ('crossDocking', 'Cross Docking'),
    ('almacenamiento', 'Almacenamiento'),
    ('flete', 'Flete'),
    ('renpre', 'RENPRE'),
    ('prueba', 'Prueba'),
    ('consultaPorPedido', 'Consulta por pedido'),
    ('consultaErronea', 'Consulta erronea'),
    ('ofreceServicio', 'Ofrece servicio'),
    ('buscaEmpleo', 'Busca empleo'),
    ]

    class Meta:
        model = FormSubmission
        fields = [
            'razon_social', 'nombre_y_apellido', 'telefono', 'servicio', 
            'estado', 'assigned_user', 'management_message'
        ]

    servicio = forms.ChoiceField(choices=SERVICIO_CHOICES, required=False)


class ManualFormSubmissionForm(forms.ModelForm):
    class Meta:
        model = FormSubmission
        fields = [
            'empresa', 'razon_social', 'nombre_y_apellido', 'servicio',
            'mail', 'telefono', 'origen', 'sub_origen', 'mensaje',
            'avance', 'estado', 'assigned_user', 'campaign'
        ]

    ORIGEN_CHOICES = [
    ('web', 'Web'),
    ('redesSociales', 'Redes Sociales'),
    ('referido', 'Referido'),
    ('exCliente', 'Ex Cliente'),
    ]
    
    # Marking some fields as required
    empresa = forms.CharField(required=True)
    estado = forms.ChoiceField(choices=ESTADO_CHOICES, required=True)
    assigned_user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=True)
    razon_social = forms.CharField(required=False)
    mail = forms.EmailField(required=False)
    origen = forms.ChoiceField(choices=ORIGEN_CHOICES, required=True)
    
    # Optional fields
    nombre_y_apellido = forms.CharField(required=False)
    telefono = forms.CharField(required=False)
    mensaje = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(ManualFormSubmissionForm, self).__init__(*args, **kwargs)

        self.fields['empresa'].help_text = "obligatorio"
        self.fields['estado'].help_text = "obligatorio"
        self.fields['assigned_user'].help_text = "obligatorio"
        self.fields['razon_social'].help_text = "obligatorio"
        self.fields['mail'].help_text = "obligatorio"

class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(label='Seleccione un archivo Excel')