# usersapp/tests/test_forms.py

from django.test import TestCase
from usersapp.forms import CustomUserCreationForm, UserProfileUpdateForm, CustomPasswordChangeForm
from usersapp.models import CustomUser

class CustomUserCreationFormTest(TestCase):

    def test_valid_form(self):
        """Test valid CustomUserCreationForm"""
        form_data = {
            'username': 'newuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'role': CustomUser.EMPLOYEE,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_password_mismatch(self):
        """Test invalid form with password mismatch"""
        form_data = {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'differentpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['Las contraseñas no coinciden.'])

class UserProfileUpdateFormTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='profile_user',
            password='password123',
            email='initial@example.com',
            first_name='InitialFirst',
            last_name='InitialLast',
            phone_number='123456789'
        )

    def test_valid_profile_update_form(self):
        """Test valid UserProfileUpdateForm"""
        form_data = {
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
            'email': 'updated@example.com',
            'phone_number': '987654321',
        }
        form = UserProfileUpdateForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.first_name, 'UpdatedFirst')
        self.assertEqual(updated_user.email, 'updated@example.com')

class CustomPasswordChangeFormTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='password_user',
            password='oldpassword123'
        )

    def test_password_change_valid(self):
        """Test CustomPasswordChangeForm with valid data"""
        form_data = {
            'old_password': 'oldpassword123',
            'new_password1': 'newpassword456',
            'new_password2': 'newpassword456',
        }
        form = CustomPasswordChangeForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_change_invalid_old_password(self):
        """Test CustomPasswordChangeForm with incorrect old password"""
        form_data = {
            'old_password': 'wrongoldpassword',
            'new_password1': 'newpassword456',
            'new_password2': 'newpassword456',
        }
        form = CustomPasswordChangeForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('old_password', form.errors)
        self.assertEqual(form.errors['old_password'], ['La contraseña actual es incorrecta.'])