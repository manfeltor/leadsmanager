from django import forms
from .models import FormSubmission, ESTADO_CHOICES
from usersapp.models import CustomUser

class FormSubmissionEditForm(forms.ModelForm):
    assigned_user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role='employee'), required=False)

    class Meta:
        model = FormSubmission
        fields = [
            'razon_social', 'nombre_y_apellido', 'telefono', 
            'estado', 'assigned_user', 'management_message'
        ]

class ManualFormSubmissionForm(forms.ModelForm):
    class Meta:
        model = FormSubmission
        fields = [
            'empresa', 'razon_social', 'nombre_y_apellido', 'servicio',
            'mail', 'telefono', 'origen', 'sub_origen', 'mensaje',
            'avance', 'estado', 'assigned_user', 'campaign'
        ]
    
    # Marking some fields as required
    empresa = forms.CharField(required=True)
    estado = forms.ChoiceField(choices=ESTADO_CHOICES, required=True)
    assigned_user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=True)
    razon_social = forms.CharField(required=False)
    mail = forms.EmailField(required=False)
    
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