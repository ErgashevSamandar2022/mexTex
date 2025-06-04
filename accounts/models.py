from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Foydalanuvchi'),
        ('taqrizchi_inf1', 'Jo\'rayev Adhamjon Informatika Taqrizchisi 1-raqamli'),
        ('taqrizchi_inf2', 'Sobirov Azizber Informatika Taqrizchisi 2-raqamli'),
        ('taqrizchi_inf3', 'Xasanov Saredor Informatika Taqrizchisi 3-raqamli'),
        ('taqrizchi_iq1', 'Ergasheva Halima Iqtisod Taqrizchisi 1-raqamli'),
        ('taqrizchi_iq2', 'Muhammadaliyev Zuhriddin Iqtisod Taqrizchisi 2-raqamli'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username

@receiver(post_save, sender=CustomUser)
def set_default_role(sender, instance, created, **kwargs):
    if created:
        instance.role = 'user'
        instance.save()