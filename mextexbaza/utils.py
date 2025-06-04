# mextexbaza/utils.py

from mextexbaza.models import Article, ArxivArticle

def archive_article(article):
    # ArxivArticle modelida bitta Articlega mos keladigan yozuvni qidirish
    arxiv_article, created = ArxivArticle.objects.get_or_create(
        title=article.title,
        nashr_yili=article.nashr_yili,
        nashr_soni=article.nashr_soni,
        defaults={
            'num': article.num,
            'num1': article.num1,
            'image': article.image,  
            'file': article.file,
            'archived': True
        }
    )

    # Agar Articleda fayl o'zgargan bo'lsa, ArxivArticle modelidagi faylni yangilash
    if article.file and arxiv_article.file != article.file:
        arxiv_article.file = article.file
        arxiv_article.save()
