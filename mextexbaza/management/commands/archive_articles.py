from django.core.management.base import BaseCommand
from mextexbaza.models import Article, ArxivArticle

class Command(BaseCommand):
    help = 'Archives all articles to ArxivArticle model'

    def handle(self, *args, **kwargs):
        # Barcha Article ma'lumotlarini olish
        articles = Article.objects.all()

        for article in articles:
            # Har bir Article uchun yangi ArxivArticle yozish
            ArxivArticle.objects.create(
                title=article.title,
                nashr_yili=article.nashr_yili,
                nashr_soni=article.nashr_soni,
                num=article.num,
                num1=article.num1,
                image=article.image,
                file=article.file,
                archived=True  # Arxivga qo'shilganini belgilash
            )

        self.stdout.write(self.style.SUCCESS('Successfully archived all articles'))
