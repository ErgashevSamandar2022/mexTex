from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from datetime import datetime

from mextexbaza.models import Article, TastiqlanganMaqola
from boglanish.models import Maqola, NewMessage
from accounts.models import CustomUser

User = get_user_model()

class BlogViewsTest(TestCase):
    def setUp(self):
        # Test foydalanuvchilari
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='user'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            role='admin'
        )
        
        # Test maqolalari
        self.article = Article.objects.create(
            title='Test Article',
            content='Test content'
        )
        
        self.maqola = Maqola.objects.create(
            sarlavha='Test Maqola',
            muallif='Test Muallif',
            matn='Test matn',
            foydalanuvchi=self.user
        )
        
        self.client = Client()

    def test_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(len(response.context['articles']), 1)
        self.assertEqual(response.context['articles'][0].title, 'Test Article')
        self.assertEqual(response.context['yil_count'], datetime.now().year - 2020)
        self.assertEqual(response.context['oqituvchi_count'], 2)
        self.assertEqual(response.context['jurnal_count'], 1)

    def test_about_page_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_message_page_view(self):
        response = self.client.get(reverse('message'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'message.html')
        self.assertEqual(len(response.context['maqolalar']), 1)
        self.assertEqual(response.context['maqolalar'][0].sarlavha, 'Test Maqola')

    def test_foydalanuvchilar_page_access_denied(self):
        # Oddiy foydalanuvchi kirishga urinayotganida
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('foydalanuvchilar'))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_foydalanuvchilar_page_access_granted(self):
        # Admin kirishga urinayotganida
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('foydalanuvchilar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foydalanuvchi.html')
        self.assertEqual(len(response.context['users']), 2)

    def test_foydalanuvchilar_role_change(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(reverse('foydalanuvchilar'), {
            'user_id': self.user.id,
            'new_role': 'taqrizchi'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'taqrizchi')
        self.assertTrue(self.user.is_approved)

    def test_edit_article_view(self):
        initial_count = Maqola.objects.count()
        response = self.client.get(reverse('edit_article', args=[self.maqola.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after edit
        
        # TastiqlanganMaqola yaratilganligini tekshiramiz
        self.assertEqual(Maqola.objects.count(), initial_count)
        self.assertEqual(TastiqlanganMaqola.objects.count(), 1)
        self.assertEqual(TastiqlanganMaqola.objects.first().sarlavha, 'Test Maqola')

    def test_delete_article_view(self):
        initial_count = Maqola.objects.count()
        response = self.client.get(reverse('delete_article', args=[self.maqola.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after delete
        self.assertEqual(Maqola.objects.count(), initial_count - 1)

    def test_send_message_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('send_message', args=[self.maqola.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newMessage.html')
        self.assertIn('form', response.context)
        self.assertIn('maqola', response.context)

    def test_send_message_view_post(self):
        self.client.login(username='testuser', password='testpass123')
        initial_count = NewMessage.objects.count()
        response = self.client.post(reverse('send_message', args=[self.maqola.pk]), {
            'message': 'Test xabar matni'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(NewMessage.objects.count(), initial_count + 1)
        
        # Xabarning to'g'ri yaratilganligini tekshiramiz
        new_message = NewMessage.objects.last()
        self.assertEqual(new_message.from_user, self.user)
        self.assertEqual(new_message.to_user, self.user)  # Maqola muallifi ham self.user
        self.assertEqual(new_message.message, 'Test xabar matni')
        
        # Messages framework ishlayotganligini tekshiramiz
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Xabar muvaffaqiyatli yuborildi!")

    def test_send_message_no_author(self):
        # Muallifi bo'lmagan maqola uchun test
        maqola = Maqola.objects.create(
            sarlavha='No Author Maqola',
            muallif='No Author',
            matn='Test matn',
            foydalanuvchi=None  # Muallif ro'yxatdan o'tmagan
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('send_message', args=[maqola.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect with error
        
        # Xato xabari chiqqanligini tekshiramiz
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Maqola muallifi ro'yhatdan o'tmagan foydalanuvchi.")