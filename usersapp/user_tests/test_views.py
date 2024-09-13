from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class LoginViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password123'
        )
    
    def test_login_success(self):
        """Test successful login and redirection to home page"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('home'))
    
    def test_login_invalid_credentials(self):
        """Test failed login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Renders login page again
        self.assertContains(response, 'Usuario y/o contraseña inválidos')  # Error message
