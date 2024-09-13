from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from formsapp.models import FormSubmission, LeadHistory
from datetime import timedelta
from django.contrib.auth import get_user_model

class BaseViewTests(TestCase):
    def setUp(self):
        # Create a dummy FormSubmission without auto-triggering LeadHistory
        form_submission = FormSubmission.objects.create(
            estado='pendiente', fecha_creacion=timezone.now() - timedelta(days=5)
        )
        # Create the related LeadHistory explicitly
        LeadHistory.objects.create(form_submission=form_submission, change_description="Initial test entry")

    def test_base_view(self):
        """Test the base view renders correctly with calculated percentages"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')
        self.assertIn('cold_percentage', response.context)
        self.assertIn('active_percentage', response.context)
        self.assertIn('closed_percentage', response.context)
        self.assertContains(response, "Mi Dashboard")


    def test_base_view(self):
        """Test the base view renders correctly with calculated percentages"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')
        
        # Check if context data is being passed correctly
        self.assertIn('cold_percentage', response.context)
        self.assertIn('active_percentage', response.context)
        self.assertIn('closed_percentage', response.context)
        self.assertContains(response, "Mi Dashboard")  # Checking that some content is present


class CustomLoginViewTests(TestCase):
    def setUp(self):
        # Create a user for login testing
        self.user = get_user_model().objects.create_user(username='testuser', password='password123')

    def test_login_success(self):
        """Test successful login and redirection"""
        response = self.client.post(reverse('custom_login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('home'))

    def test_login_failure(self):
        """Test failed login with incorrect credentials"""
        response = self.client.post(reverse('custom_login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_login.html')
        self.assertContains(response, 'Invalid username or password')


class CategoryBreakdownViewTests(TestCase):
    def setUp(self):
        # Create dummy form submissions
        FormSubmission.objects.create(
            estado='pendiente', fecha_creacion=timezone.now() - timedelta(days=5)
        )
        FormSubmission.objects.create(
            estado='gestionExitosa', fecha_creacion=timezone.now() - timedelta(days=2)
        )

    def test_category_breakdown_view(self):
        """Test category breakdown view loads correctly"""
        response = self.client.get(reverse('category_breakdown'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_breakdown.html')
        
        # Check if context data is being passed correctly
        self.assertIn('plot_data', response.context)
        self.assertIn('trend_data_json', response.context)
        self.assertContains(response, 'Desglose de categorías')