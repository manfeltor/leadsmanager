from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from formsapp.models import FormSubmission, ESTADO_CHOICES
from django.utils import timezone
from datetime import timedelta

CustomUser = get_user_model()

class FormsAppViewsTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = CustomUser.objects.create_user(
            username='testuser', password='password123', role='employee')
        self.manager = CustomUser.objects.create_user(
            username='manageruser', password='password123', role='manager')
        
        # Create form submissions
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

    def test_forms_list_view(self):
        # Login as manager
        self.client.login(username='manageruser', password='password123')
        
        # Test with no filters applied
        response = self.client.get(reverse('forms_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Empresa')
        self.assertContains(response, 'Test RS')

        # Test filtering by estado
        response = self.client.get(reverse('forms_list'), {'estado': 'pendiente'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Empresa')

        # Test with an invalid estado filter
        response = self.client.get(reverse('forms_list'), {'estado': 'nonexistent'})
        self.assertNotContains(response, 'Test Empresa')

    def test_user_leads_view(self):
        # Login as the user
        self.client.login(username='testuser', password='password123')
        
        # Access the view
        response = self.client.get(reverse('user_leads'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Empresa')

        # Test filtering by status
        response = self.client.get(reverse('user_leads'), {'status': 'pendiente'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Empresa')

        # Test date filters
        date_from = (timezone.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        date_to = (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.get(reverse('user_leads'), {'date_from': date_from, 'date_to': date_to})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Empresa')

    def test_form_detail_view(self):
        # Login as the user
        self.client.login(username='testuser', password='password123')

        # Access the form detail view
        response = self.client.get(reverse('form_detail', args=[self.form_submission.submission_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Empresa')

    def test_form_edit_view(self):
        # Login as a manager
        self.client.login(username='manageruser', password='password123')

        # Access the form edit view
        response = self.client.get(reverse('form_edit', args=[self.form_submission.submission_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Empresa')

        # Test form submission (edit)
        form_data = {
            'razon_social': 'Updated RS',
            'estado': 'asignado',
            'assigned_user': self.user.id,
        }
        response = self.client.post(reverse('form_edit', args=[self.form_submission.submission_id]), form_data)
        self.assertEqual(response.status_code, 302)  # Redirects on success
        updated_form = FormSubmission.objects.get(pk=self.form_submission.pk)
        self.assertEqual(updated_form.razon_social, 'Updated RS')
        self.assertEqual(updated_form.estado, 'asignado')

    def test_manual_form_submission_view(self):
        # Login as a user
        self.client.login(username='manageruser', password='password123')

        # Access the manual form submission view
        response = self.client.get(reverse('manual_form_submission'))
        self.assertEqual(response.status_code, 200)

        # Test form submission
        form_data = {
            'empresa': 'Manual Empresa',
            'razon_social': 'Manual RS',
            'nombre_y_apellido': 'Manual NA',
            'servicio': 'Manual Servicio',
            'mail': 'manual@example.com',
            'telefono': '9876543210',
            'origen': 'Web',
            'sub_origen': 'Signos',
            'mensaje': 'Manual Mensaje',
            'avance': 'Manual Avance',
            'estado': 'asignado',
            'assigned_user': self.user.id,
            'campaign': '',
        }
        response = self.client.post(reverse('manual_form_submission'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirects on success
        new_form = FormSubmission.objects.latest('submission_id')
        self.assertEqual(new_form.empresa, 'Manual Empresa')
        self.assertEqual(new_form.estado, 'asignado')