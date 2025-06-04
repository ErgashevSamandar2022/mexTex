from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Article, ArxivArticle, TastiqlanganMaqola
from django.urls import reverse_lazy
from .forms import ArticleForm
from mextexbaza.utils import archive_article
from django.conf import settings
import os
import zipfile
from django.http import HttpResponse
from .utils import archive_article
from datetime import datetime

# from django.shortcuts import get_object_or_404, redirect
# from django.contrib import messages

# Maqolalar ro‘yxati sahifasi
from datetime import datetime
from django.views.generic import ListView
from .models import Article

class JournalPagesViews(ListView):
    model = Article
    template_name = 'toplamJournal.html'
    context_object_name = 'articles'

    def get_queryset(self):
        selected_year = self.request.GET.get('year', '')
        current_year = datetime.now().year

        # Hamma maqolalarni olayapmiz
        queryset = Article.objects.order_by('-id')

        # Eski maqolalarni ajratib olib, arxivga ko‘chirish
        for article in queryset:
            if current_year - article.nashr_yili >= 2:
                # Arxivga qo‘shamiz
                from .models import ArxivArticle  # Arxiv modelingiz shu bo‘lsa
                ArxivArticle.objects.create(
                    title=article.title,
                    nashr_yili=article.nashr_yili,
                    nashr_soni=article.nashr_soni,
                    num=article.num,
                    num1=article.num1,
                    image=article.image,
                    file=article.file,
                )
                article.delete()  # Asosiy bazadan o‘chiramiz

        # Faqat so‘nggi 2 yillik maqolalarni qaytarish
        queryset = Article.objects.filter(nashr_yili__gte=current_year - 1).order_by('-id')

        # Agar filtrlangan yili tanlangan bo‘lsa
        if selected_year and selected_year != "0":
            queryset = queryset.filter(nashr_yili=selected_year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = datetime.now().year
        selected_year = self.request.GET.get('year', '')
        if selected_year.isdigit():
            selected_year = int(selected_year)

        # Faqat so‘nggi 2 yillik maqolalar yillari
        context['selected_year'] = selected_year
        context['years'] = (
            Article.objects
            .filter(nashr_yili__gte=current_year - 1)
            .exclude(nashr_yili__isnull=True)
            .values_list('nashr_yili', flat=True)
            .distinct()
            .order_by('-nashr_yili')
        )
        return context


# Maqolani tahrirlash sahifasi
class JournalEditViews(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'journalUpdate.html'
    success_url = reverse_lazy('journals')

# Maqolani o‘chirish sahifasi
class JournalDeleteViews(DeleteView):
    model = Article
    template_name = 'journalDelete.html'
    success_url = reverse_lazy('journals')

# Yangi maqola yaratish sahifasi
class JournalCreateViews(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'journalCreate.html'
    success_url = reverse_lazy('journals')

class ArxivPagesViews(TemplateView):
    template_name = 'arxiv.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Barcha Article ma'lumotlarini olish
        articles = Article.objects.all()

        for article in articles:
            # Articledagi faylni ArxivArticle modeliga nusxalash yoki yangilash
            archive_article(article)

        # ArxivArticle modelidan ma'lumot olish
        arxiv_data = ArxivArticle.objects.all().order_by('nashr_yili')

        # Yillarni tartib bilan olish
        years = sorted(set(article.nashr_yili for article in arxiv_data), reverse=True)

        # Yillarni va ularning tegishli ma'lumotlarini birlashtirish
        year_articles = {}
        for year in years:
            year_articles[year] = [article for article in arxiv_data if article.nashr_yili == year]

        context['year_articles'] = year_articles
        return context

def arxiv_view(request):
    # ArxivArticle modelidan ma'lumotlarni olish
    arxiv_data = ArxivArticle.objects.all()

    return render(request, 'arxiv.html', {'arxiv_data': arxiv_data})


from django.db.models import Q
def tastiqMaqolalar_royxati(request):
    search_query = request.GET.get('q', '')  # q = query
    maqolalar = TastiqlanganMaqola.objects.all().order_by('-yaratilgan_sana')  # Eng yangilar yuqorida
    if search_query:
        words = search_query.strip().lower().split()
        query = Q()
        for word in words:
            query |= Q(sarlavha__icontains=word)
            query |= Q(muallif__icontains=word)
            query |= Q(matn__icontains=word)
            query |= Q(kategoriya__icontains=word)
            query |= Q(kalit_sozlar__icontains=word)
            query |= Q(telefon_raqam__icontains=word)

        maqolalar = maqolalar.filter(query)
        
    return render(request, 'tastiqlanganMaqola.html', {'maqolalar': maqolalar,'q': search_query})