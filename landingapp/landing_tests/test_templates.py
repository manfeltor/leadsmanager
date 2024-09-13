from django.test import TestCase
from formsapp.models import FormSubmission
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse


class LandingPageTemplateTests(TestCase):
    def setUp(self):
        FormSubmission.objects.create(
            estado='pendiente', fecha_creacion=timezone.now() - timedelta(days=5)
        )

    def test_landing_page_template_render(self):
        """Test that the landing page is rendered with correct dynamic content"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')
        
        # Check for dynamic content in the template
        self.assertContains(response, 'Mi Dashboard')
        self.assertIn('total_submissions', response.context)


class CustomLoginTemplateTests(TestCase):
    def test_custom_login_template_render(self):
        """Test that the login page is rendered and contains the correct elements"""
        response = self.client.get(reverse('custom_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_login.html')

        # Try printing the actual response content to inspect it
        print(response.content.decode())

        # Adjust the assertion to match the actual HTML if necessary
        self.assertContains(response, 'type="password"')


class CategoryBreakdownTemplateTests(TestCase):
    def setUp(self):
        FormSubmission.objects.create(
            estado='pendiente', fecha_creacion=timezone.now() - timedelta(days=5)
        )

    def test_category_breakdown_template_render(self):
        """Test that the category breakdown page is rendered correctly with dynamic content"""
        response = self.client.get(reverse('category_breakdown'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_breakdown.html')
        
        # Check for dynamic content in the breakdown template
        self.assertContains(response, 'Desglose de categorías')
        self.assertContains(response, '<div id="trendChart">')  # Check if the trend chart placeholder is present