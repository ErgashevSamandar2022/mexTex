from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.signals import post_save

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='user'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'user')
        self.assertFalse(self.user.is_approved)
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)

    def test_admin_creation(self):
        self.assertEqual(self.admin.username, 'admin')
        self.assertEqual(self.admin.role, 'admin')
        self.assertTrue(self.admin.is_staff)
        self.assertTrue(self.admin.is_superuser)

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_default_role_signal(self):
        """Test qo'shimcha signal ishlayotganligini tekshiramiz"""
        new_user = User.objects.create_user(
            username='signaluser',
            password='testpass123'
        )
        self.assertEqual(new_user.role, 'user')


class CustomUserFormsTest(TestCase):
    def test_user_creation_form(self):
        form_data = {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'email': 'new@example.com'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.role, 'user')

    def test_user_creation_form_with_role(self):
        """Admin tomonidan foydalanuvchi yaratishda role tanlash"""
        form_data = {
            'username': 'admin_created',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'email': 'admin_created@example.com',
            'role': 'taqrizchi'
        }
        form = CustomUserCreationForm(data=form_data, initial={'is_superuser': True})
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.role, 'taqrizchi')

    def test_user_change_form(self):
        user = User.objects.create_user(
            username='changeuser',
            password='testpass123'
        )
        form_data = {
            'username': 'changeuser',
            'email': 'changed@example.com',
            'first_name': 'Changed',
            'last_name': 'User',
            'role': 'taqrizchi'
        }
        form = CustomUserChangeForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        user.refresh_from_db()
        self.assertEqual(user.role, 'taqrizchi')
        self.assertEqual(user.email, 'changed@example.com')


class CustomUserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.home_url = '/'  # O'zgartiring kerak bo'lsa
        self.user_data = {
            'username': 'testviewuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'testview@example.com'
        }

    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_signup_view_post_success(self):
        response = self.client.post(self.signup_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, self.home_url)
        
        # Foydalanuvchi yaratilganligini tekshiramiz
        user = User.objects.get(username='testviewuser')
        self.assertEqual(user.role, 'user')
        self.assertEqual(user.email, 'testview@example.com')

    def test_signup_view_post_invalid(self):
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'differentpassword'
        response = self.client.post(self.signup_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', "The two password fields didn't match.")


class CustomUserAdminTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        self.client = Client()
        self.client.force_login(self.admin)

    def test_admin_list_display(self):
        response = self.client.get('/admin/accounts/customuser/')
        self.assertContains(response, 'username')
        self.assertContains(response, 'email')
        self.assertContains(response, 'role')

    def test_admin_add_user(self):
        response = self.client.post(
            '/admin/accounts/customuser/add/',
            {
                'username': 'newadminuser',
                'password1': 'complexpass123',
                'password2': 'complexpass123',
                'email': 'newadmin@example.com',
                'role': 'taqrizchi',
                'is_staff': 'on'
            }
        )
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username='newadminuser')
        self.assertEqual(new_user.role, 'taqrizchi')
        self.assertTrue(new_user.is_staff)