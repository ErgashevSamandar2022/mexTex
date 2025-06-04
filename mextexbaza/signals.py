# mextexbaza/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article
from .utils import archive_article

@receiver(post_save, sender=Article)
def archive_article_signal(sender, instance, created, **kwargs):
    if created:
        archive_article(instance)
