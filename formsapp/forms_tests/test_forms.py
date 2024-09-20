from django.test import TestCase
from formsapp.forms import FormSubmissionEditForm, ManualFormSubmissionForm
from formsapp.models import FormSubmission, CustomUser, ESTADO_CHOICES
from django.utils import timezone

class FormsAppFormsTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser', password='password123', role='employee')

        # Create another user (manager)
        self.manager = CustomUser.objects.create_user(
            username='manageruser', password='password123', role='manager')

        # Create a form submission object
        self.form_submission = FormSubmission.objects.create(
            empresa='Test Empresa',
            fecha_creacion=timezone.now(),
            razon_social='Test RS',
            nombre_y_apellido='Test NA',
            servicio='Test Servicio',
            mail='test@example.com',
            telefono='1234567890',
            origen='Web',
            sub_origen='Signos',
            mensaje='Test Mensaje',
            avance='Test Avance',
            estado='pendiente',
            form_id=1,
            submission_id=1,
            assigned_user=self.user
        )

    def test_form_submission_edit_form_valid(self):
        """Test valid FormSubmissionEditForm"""
        form_data = {
            'razon_social': 'Updated RS',
            'nombre_y_apellido': 'Updated NA',
            'telefono': '9876543210',
            'estado': 'contactado',
            'assigned_user': self.manager.id,
            'management_message': 'Updated message'
        }

        form = FormSubmissionEditForm(data=form_data, instance=self.form_submission)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.form_submission.razon_social, 'Updated RS')
        self.assertEqual(self.form_submission.estado, 'contactado')
        self.assertEqual(self.form_submission.assigned_user, self.manager)

    def test_form_submission_edit_form_invalid(self):
        """Test invalid FormSubmissionEditForm with missing required fields"""
        form_data = {
            'razon_social': '',  # Missing razon_social
            'estado': 'contactado'
        }

        form = FormSubmissionEditForm(data=form_data, instance=self.form_submission)
        self.assertFalse(form.is_valid())
        self.assertIn('razon_social', form.errors)

    def test_manual_form_submission_form_valid(self):
        """Test valid ManualFormSubmissionForm"""
        form_data = {
            'empresa': 'New Empresa',
            'razon_social': 'New RS',
            'nombre_y_apellido': 'New NA',
            'servicio': 'New Servicio',
            'mail': 'new@example.com',
            'telefono': '1122334455',
            'origen': 'Web',
            'sub_origen': 'Signos',
            'mensaje': 'New Mensaje',
            'avance': 'New Avance',
            'estado': 'pendiente',
            'assigned_user': self.manager.id,
            'campaign': None  # Optional field
        }

        form = ManualFormSubmissionForm(data=form_data)
        self.assertTrue(form.is_valid())
        submission = form.save(commit=False)
        submission.fecha_creacion = timezone.now()  # Set the creation date manually
        submission.save(user=self.user)
        self.assertEqual(submission.empresa, 'New Empresa')
        self.assertEqual(submission.assigned_user, self.manager)

    def test_manual_form_submission_form_invalid(self):
        """Test invalid ManualFormSubmissionForm with missing required fields"""
        form_data = {
            'empresa': '',  # Missing empresa (required)
            'razon_social': 'New RS',
            'estado': 'pendiente'
        }

        form = ManualFormSubmissionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('empresa', form.errors)  # Ensure 'empresa' is flagged as required