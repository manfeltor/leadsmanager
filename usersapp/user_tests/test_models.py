# usersapp/tests/test_models.py

from django.test import TestCase
from usersapp.models import CustomUser, UserAttribute

class CustomUserModelTest(TestCase):

    def setUp(self):
        self.employee_user = CustomUser.objects.create_user(
            username='employee_user',
            password='password123',
            role=CustomUser.EMPLOYEE
        )
        self.manager_user = CustomUser.objects.create_user(
            username='manager_user',
            password='password123',
            role=CustomUser.MANAGER
        )

    def test_user_str(self):
        """Test the string representation of the CustomUser model"""
        self.assertEqual(str(self.employee_user), 'employee_user')
        self.assertEqual(str(self.manager_user), 'manager_user')

    def test_is_management(self):
        """Test the is_management property for CustomUser"""
        self.assertFalse(self.employee_user.is_management)
        self.assertTrue(self.manager_user.is_management)

class UserAttributeModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='user_with_attribute',
            password='password123'
        )
        self.user_attribute = UserAttribute.objects.create(
            user=self.user,
            value1="Attribute 1",
            value2="Attribute 2"
        )

    def test_user_attribute_str(self):
        """Test the string representation of UserAttribute model"""
        self.assertEqual(str(self.user_attribute), 'user_with_attribute')
    
    def test_user_attribute_relationship(self):
        """Test the relationship between UserAttribute and CustomUser"""
        self.assertEqual(self.user_attribute.user, self.user)