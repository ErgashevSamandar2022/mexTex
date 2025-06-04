from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # YANGI QO‘SHILDI
    name = models.CharField(max_length=100, verbose_name="Ism",blank=False, null=True)
    email = models.EmailField(verbose_name="Elektron pochta",blank=False, null=True)
    message = models.TextField(verbose_name="Xabar",blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    def __str__(self):
        return str(self.name or "Ismsiz")

class Maqola(models.Model):
    CATEGORY_CHOICES = [
        ('texnologiya', 'Texnologiya'),
        ('talim', 'Ta\'lim'),
        ('tibbiyot', 'Tibbiyot'),
        ('iqtisod', 'Iqtisodiyot'),
        ('boshqa', 'Boshqalar'),
    ]
    STATUS_CHOICES = [
        ('tekshirilmoqda', 'Tekshirilmoqda'),
        ('tasdiqlandi', 'Tasdiqlandi'),
        ('rad_etildi', 'Rad etildi'),
    ]
    
    sarlavha = models.CharField(max_length=200, verbose_name="Maqola mavzusi", blank=False)
    muallif = models.CharField(max_length=100, verbose_name="Muallif", blank=False)
    matn = models.TextField(verbose_name="Maqola anotatsiyasi", blank=False)
    kategoriya = models.CharField(max_length=100, verbose_name="Kategoriya", blank=False, choices=CATEGORY_CHOICES)
    kalit_sozlar = models.CharField(max_length=200, blank=True, verbose_name="Kalit so‘zlar")
    telefon_raqam = models.CharField(max_length=20, verbose_name="Bog‘lanish uchun telefon raqam", blank=True, null=True)  # <-- o'zgargan qism
    fayl = models.FileField(upload_to='maqola_fayllar/', blank=True, null=True, verbose_name="Maqola fayl")
    yaratilgan_sana = models.DateTimeField(default=timezone.now, verbose_name="Yaratilgan sana")
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Yuklovchi foydalanuvchi")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='tekshirilmoqda',
        verbose_name="Holat"
    )
    
    def __str__(self):
        return self.sarlavha
    
    
class NewMessage(models.Model):
    from_user = models.ForeignKey(get_user_model(), related_name='sent_messages', on_delete=models.CASCADE)
    to_user = models.ForeignKey(get_user_model(), related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Xabar: {self.message[:50]}... {self.from_user.username} -> {self.to_user.username}"
    
    
class MaqolaYuborishLog(models.Model):
    maqola = models.ForeignKey('Maqola', on_delete=models.CASCADE)
    kimga = models.CharField(max_length=100)
    yuborilgan_vaqt = models.DateTimeField(auto_now_add=True)
    holat = models.BooleanField(null=True, blank=True)  # True=Qabul, False=Rad, None=javob berilmagan
    javob_berilgan = models.BooleanField(default=False)  # Admin ko‘rishi uchun

    def __str__(self):
        return f"{self.maqola} -> {self.kimga}"