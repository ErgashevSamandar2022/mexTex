from django.views.generic import ListView,TemplateView
from mextexbaza.models import Article
from accounts.models import CustomUser
from boglanish.models import Maqola
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

from django.utils.translation import gettext as _

def home(request):
    context = {
        "welcome_text": _("Welcome to our website!"),
    }
    return render(request, "index.html", context)
  
  
class HomePagesViews(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Oxirgi 4 ta maqola
        context['articles'] = Article.objects.order_by('-id')[:4]

        # Statistik ma'lumotlar
        start_year = 2020
        current_year = datetime.now().year
        yil_count = current_year - start_year

        oqituvchi_count = User.objects.count()  # endi CustomUser asosida ishlaydi
        jurnal_count = Article.objects.count()

        # Kontekstga qo‘shish
        context['yil_count'] = yil_count
        context['oqituvchi_count'] = oqituvchi_count
        context['jurnal_count'] = jurnal_count

        return context

class AboutPagesViews(TemplateView):
  template_name = 'about.html'

  
class ContactPagesViews(TemplateView):
  template_name = 'boglanish.html'
  
class MessagePagesViews(ListView):
    model = Maqola
    template_name = "message.html"
    context_object_name = "maqolalar"


import os
from django.conf import settings

def delete_article(request, pk):
    maqola = get_object_or_404(Maqola, pk=pk)

    # # Fayllarni o‘chirish
    # if maqola.rasm:
    #     if os.path.isfile(maqola.rasm.path):
    #         os.remove(maqola.rasm.path)

    if maqola.fayl:
        if os.path.isfile(maqola.fayl.path):
            os.remove(maqola.fayl.path)

    maqola.delete()
    return redirect('message')


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from boglanish.models import NewMessage
from boglanish.forms import MessageForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.contrib.auth.models import User  # Foydalanuvchi modelini olish

User = get_user_model()

@login_required
def send_message(request, pk):
    maqola = get_object_or_404(Maqola, pk=pk)

    if not maqola.foydalanuvchi:
        messages.error(request, "Maqola muallifi ro'yhatdan o'tmagan foydalanuvchi.")
        return redirect('message')  # mavjud nomdagi sahifaga qaytarish

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            NewMessage.objects.create(
                from_user=request.user,
                to_user=maqola.foydalanuvchi,
                message=form.cleaned_data['message']
            )
            messages.success(request, "Xabar muvaffaqiyatli yuborildi!")
            return redirect('message')  # yoki kerakli sahifa nomi
    else:
        form = MessageForm()

    return render(request, 'newMessage.html', {'form': form, 'maqola': maqola})

  
# class NewMessagePagesViews(TemplateView):
#   template_name = 'newMessage.html'

class JournalMessagePagesViews(TemplateView):
  template_name = 'journal_message.html'

class FoydalanuvchiPagesViews(UserPassesTestMixin, View):
    template_name = 'foydalanuvchi.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff # Faqat adminlar kirishi mumkin

    def get(self, request):
        search_query = request.GET.get('q', '').strip()
        users = CustomUser.objects.all()  # Barcha foydalanuvchilarni olish
        
        if search_query:
            words = search_query.lower().split()
            query = Q()
            for word in words:
                query |= Q(username__icontains=word)
                query |= Q(email__icontains=word)
                query |= Q(role__icontains=word)
            users = users.filter(query)

        return render(request, self.template_name, {
            'users': users,
            'q': search_query  # inputda qidiruvni ko‘rsatish uchun
        })
        # return render(request, self.template_name, {'users': users})

    def post(self, request):
        user_id = request.POST.get('user_id')  # Foydalanuvchi ID'sini olish
        new_role = request.POST.get('new_role')  # Yangi rolni olish
        user = CustomUser.objects.get(id=user_id)  # Foydalanuvchini olish
        
        user.role = new_role  # Rolni yangilash
        
        # Agar foydalanuvchi admin yoki taqrizchi bo'lsa, is_approved True qilish
        if new_role in ['admin', 'taqrizchi']:
            user.is_approved = True
        else:
            user.is_approved = False
        
        user.save()  # Foydalanuvchini saqlash

        return redirect('foydalanuvchilar')  # 'foydalanuvchilar' nomli sahifaga qaytish
    
    
@login_required
def my_articles_view(request):
    search_query = request.GET.get('q', '').strip()
    articles = Maqola.objects.filter(foydalanuvchi=request.user).order_by('-yaratilgan_sana')
    
    if search_query:
            words = search_query.lower().split()
            query = Q()
            for word in words:
                query |= Q(muallif__icontains=word)
                query |= Q(sarlavha__icontains=word)
                query |= Q(kategoriya__icontains=word)
                query |= Q(kalit_sozlar__icontains=word)
                
            articles = articles.filter(query)


    return render(request, 'my_articles.html', {'articles': articles,'q':search_query})