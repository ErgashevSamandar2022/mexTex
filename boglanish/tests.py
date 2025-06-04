from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages

from .models import Contact, Maqola, NewMessage
from .forms import ContactForm, MaqolaForm, MessageForm

User = get_user_model()

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )

    def test_contact_model(self):
        contact = Contact.objects.create(
            user=self.user1,
            name='Test User',
            email='test@example.com',
            message='Test message'
        )
        self.assertEqual(str(contact), 'Test User')
        self.assertEqual(contact.user.username, 'user1')
        self.assertTrue(contact.created_at is not None)

    def test_maqola_model(self):
        maqola = Maqola.objects.create(
            sarlavha='Test Maqola',
            muallif='Test Muallif',
            matn='Test matn',
            kategoriya='texnologiya',
            foydalanuvchi=self.user1
        )
        self.assertEqual(str(maqola), 'Test Maqola')
        self.assertEqual(maqola.foydalanuvchi.username, 'user1')
        self.assertEqual(maqola.kategoriya, 'texnologiya')

    def test_new_message_model(self):
        message = NewMessage.objects.create(
            from_user=self.user1,
            to_user=self.user2,
            message='Test message content'
        )
        self.assertTrue('Xabar: Test message content... user1 -> user2' in str(message))


class FormsTestCase(TestCase):
    def test_contact_form_valid(self):
        form_data = {
            'name': 'Form Test',
            'email': 'test@example.com',
            'message': 'Test message content'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid(self):
        form_data = {
            'name': '',
            'email': 'not-an-email',
            'message': ''
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_maqola_form_valid(self):
        test_file = SimpleUploadedFile("test.txt", b"file_content")
        test_image = SimpleUploadedFile("test.jpg", b"file_content")
        
        form_data = {
            'sarlavha': 'Test Maqola',
            'muallif': 'Test Muallif',
            'matn': 'Test matn',
            'kategoriya': 'texnologiya',
            'kalit_sozlar': 'test, maqola'
        }
        form = MaqolaForm(data=form_data, files={
            'rasm': test_image,
            'fayl': test_file
        })
        self.assertTrue(form.is_valid())

    def test_message_form(self):
        form_data = {
            'message': 'Test message content'
        }
        form = MessageForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )
        
        # Test ma'lumotlari
        self.contact = Contact.objects.create(
            user=self.user1,
            name='Test User',
            email='test@example.com',
            message='Test message'
        )
        
        self.maqola = Maqola.objects.create(
            sarlavha='Test Maqola',
            muallif='Test Muallif',
            matn='Test matn',
            kategoriya='texnologiya',
            foydalanuvchi=self.user1
        )
        
        self.message = NewMessage.objects.create(
            from_user=self.user1,
            to_user=self.user2,
            message='Test message content'
        )

    def test_boglanish_view_get(self):
        response = self.client.get(reverse('boglanish'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'boglanish.html')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_boglanish_view_post(self):
        form_data = {
            'name': 'New Contact',
            'email': 'new@example.com',
            'message': 'New message content'
        }
        response = self.client.post(reverse('boglanish'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 2)

    def test_journal_message_view(self):
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('journal_message'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal_message.html')
        self.assertEqual(len(response.context['messages']), 1)

    def test_maqola_yuborish_view_get(self):
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('maqola_yuborish'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'maqola.html')
        self.assertIsInstance(response.context['form'], MaqolaForm)

    def test_maqola_yuborish_view_post(self):
        self.client.login(username='user1', password='testpass123')
        test_file = SimpleUploadedFile("test.txt", b"file_content")
        test_image = SimpleUploadedFile("test.jpg", b"file_content")
        
        form_data = {
            'sarlavha': 'New Maqola',
            'muallif': 'New Muallif',
            'matn': 'New matn',
            'kategoriya': 'talim',
            'kalit_sozlar': 'new, test'
        }
        response = self.client.post(reverse('maqola_yuborish'), {
            **form_data,
            'rasm': test_image,
            'fayl': test_file
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Maqola.objects.count(), 2)
        self.assertTrue(response.context['success'])

    def test_maqolalar_royxati_view(self):
        response = self.client.get(reverse('maqola_message'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'message.html')
        self.assertEqual(len(response.context['maqolalar']), 1)

    def test_inbox_view(self):
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sendMessage.html')
        self.assertEqual(len(response.context['xabarlar']), 1)

    def test_contact_message_view(self):
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('contactMess'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contactMessage.html')
        self.assertEqual(len(response.context['conMessage']), 1)


class AdminTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        self.client = Client()
        self.client.force_login(self.admin)
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.contact = Contact.objects.create(
            user=self.user,
            name='Test User',
            email='test@example.com',
            message='Test message'
        )
        self.maqola = Maqola.objects.create(
            sarlavha='Test Maqola',
            muallif='Test Muallif',
            matn='Test matn',
            kategoriya='texnologiya',
            foydalanuvchi=self.user
        )
        self.message = NewMessage.objects.create(
            from_user=self.user,
            to_user=self.admin,
            message='Test message content'
        )

    def test_contact_admin(self):
        response = self.client.get('/admin/boglanish/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')

    def test_maqola_admin(self):
        response = self.client.get('/admin/boglanish/maqola/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Maqola')

    def test_new_message_admin(self):
        response = self.client.get('/admin/boglanish/newmessage/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test message content')