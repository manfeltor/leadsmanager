from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from formsapp.models import FormSubmission
from django.utils import timezone

CustomUser = get_user_model()

class FormsAppTemplatesTest(TestCase):

    def setUp(self):
        # Create a user and form submission
        self.user = CustomUser.objects.create_user(
            username='testuser', password='password123', role='employee')
        self.manager = CustomUser.objects.create_user(
            username='manageruser', password='password123', role='manager')
        
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

    def test_forms_list_template_render(self):
        # Login as a manager
        self.client.login(username='manageruser', password='password123')

        # Access the form list view
        response = self.client.get(reverse('forms_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_forms_submissions.html')
        self.assertContains(response, 'Test Empresa')
        self.assertContains(response, 'Test RS')

    def test_user_leads_template_render(self):
        # Login as the user
        self.client.login(username='testuser', password='password123')

        # Access the user leads view
        response = self.client.get(reverse('user_leads'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_leads_list.html')
        self.assertContains(response, 'Test Empresa')
        self.assertContains(response, 'Test NA')

    def test_form_detail_template_render(self):
        # Login as the user
        self.client.login(username='testuser', password='password123')

        # Access the form detail view
        response = self.client.get(reverse('form_detail', args=[self.form_submission.submission_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_detail.html')
        self.assertContains(response, 'Test Empresa')
        self.assertContains(response, 'Test Mensaje')

    def test_form_edit_template_render(self):
        # Login as a manager
        self.client.login(username='manageruser', password='password123')

        # Access the form edit view
        response = self.client.get(reverse('form_edit', args=[self.form_submission.submission_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_edit.html')
        self.assertContains(response, 'Test Empresa')
        self.assertContains(response, 'estado')

    def test_manual_form_submission_template_render(self):
        # Login as a manager
        self.client.login(username='manageruser', password='password123')

        # Access the manual form submission view
        response = self.client.get(reverse('manual_form_submission'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manual_form_submission.html')
        self.assertContains(response, 'Manual Form Submission')
        self.assertContains(response, 'empresa')
        self.assertContains(response, 'razon_social')