from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=200)
    nashr_yili = models.IntegerField()
    nashr_soni = models.IntegerField()
    num = models.CharField(max_length=100)
    num1 = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    file = models.FileField(upload_to='files/')
    
    def __str__(self):
        return self.title

class ArxivArticle(models.Model):
    title = models.CharField(max_length=200)
    nashr_yili = models.IntegerField()
    nashr_soni = models.IntegerField()
    num = models.CharField(max_length=100)
    num1 = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    file = models.FileField(upload_to='files/')
    archived = models.BooleanField(default=True)  # Bu ma'lumotni arxivga ko'chirilganligini bildiradi
    
    def __str__(self):
        return self.title
    
    
class TastiqlanganMaqola(models.Model):
    # username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    sarlavha = models.CharField(max_length=200, verbose_name="Maqola mavzusi",blank=False)
    muallif = models.CharField(max_length=100, verbose_name="Muallif",blank=False)
    matn = models.TextField(verbose_name="Maqola matni",blank=False, default="Matn mavjud emas")
    kategoriya = models.CharField(max_length=100, verbose_name="Kategoriya",blank=False)
    kalit_sozlar = models.CharField(max_length=200, blank=True, verbose_name="Kalit so‘zlar",)
    telefon_raqam = models.CharField(max_length=20, verbose_name="Bog‘lanish uchun telefon raqam", blank=True, null=True)  # <-- o'zgargan qism
    fayl = models.FileField(upload_to='tasdiqlangan_fayllar/', blank=True, null=True)
    yaratilgan_sana = models.DateTimeField()

    def __str__(self):
        return self.sarlavha
    
    