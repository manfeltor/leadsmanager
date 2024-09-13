from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

class ProfileTemplateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password123', email='test@example.com'
        )
    
    def test_profile_template_used(self):
        """Test profile template is rendered with correct user data"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_detail.html')
        self.assertContains(response, 'testuser')  # Check if username is displayed
        self.assertContains(response, 'test@example.com')  # Check if email is displayed

class UnauthorizedTemplateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password123'
        )
    
    def test_unauthorized_template_rendered(self):
        """Test unauthorized template is used for restricted access"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('unauthorized'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'unauthorized.html')
        self.assertContains(response, 'Acceso no autorizado')  # Check for the message in the template