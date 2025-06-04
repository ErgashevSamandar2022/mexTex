from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from .models import NewMessage, Contact, Maqola
from .forms import MaqolaForm, ContactForm, MessageForm
from mextexbaza.models import Article
from django.urls import reverse_lazy
from django.urls import reverse

from mextexbaza.models import TastiqlanganMaqola
from .models import Maqola
import os
from django.conf import settings
from .forms import MessageForm
from django.db.models import Q

class ContactPagesViews(ListView):
    model = Contact
    template_name = "boglanish.html"
    context_object_name = "boglanish"
    

def boglanish(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user  # foydalanuvchini biriktiryapmiz
            contact.save()
    else:
        form = ContactForm()
    return render(request, 'boglanish.html', {'form': form})   


def journal_message(request):
    messages = NewMessage.objects.filter(to_user=request.user).order_by('-created_at')
    return render(request, 'journal_message.html', {'messages': messages})

def maqola_yuborish(request):
    if request.method == 'POST':
        form = MaqolaForm(request.POST, request.FILES)
        if form.is_valid():
            maqola = form.save(commit=False)
            maqola.foydalanuvchi = request.user
            maqola.status = 'tekshirilmoqda'
            maqola.save()
            return render(request, 'maqola.html', {'form': MaqolaForm(), 'success': True})
    else:
        form = MaqolaForm()
    return render(request, 'maqola.html', {'form': form})
    

def maqola_tasdiqlash(request, maqola_id):
    maqola = get_object_or_404(Maqola, id=maqola_id)
    maqola.status = 'tasdiqlandi'
    maqola.save()
    
    TastiqlanganMaqola.objects.create(
        sarlavha=maqola.sarlavha,
        muallif=maqola.muallif,
        matn=maqola.matn,
        kategoriya=maqola.kategoriya,
        kalit_sozlar=maqola.kalit_sozlar,
        telefon_raqam=maqola.telefon_raqam,
        fayl=maqola.fayl,
        yaratilgan_sana=maqola.yaratilgan_sana
    )
    
    return redirect('maqola_message')

def maqola_rad_etish(request, maqola_id):
    maqola = get_object_or_404(Maqola, id=maqola_id)
    maqola.status = 'rad_etildi'
    maqola.save()
    return redirect('maqola_message')


def maqolalar_royxati(request):
    search_query = request.GET.get('q', '')  # q = query
    maqolalar = Maqola.objects.all().order_by('-yaratilgan_sana')
    
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

    return render(request, 'message.html', {'maqolalar': maqolalar, 'q': search_query})

def inbox(request):
    # user = request.user
    xabarlar = NewMessage.objects.all().order_by('-created_at')
    return render(request, 'sendMessage.html', {'xabarlar': xabarlar})

def contactMessage(request):
    conMessage=Contact.objects.all().order_by('-created_at')
    return render(request, 'contactMessage.html', {'conMessage': conMessage})


from .forms import RoleSelectionForm
from accounts.models import CustomUser
from .models import MaqolaYuborishLog
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def maqola_send_taqriz(request, maqola_id):
    maqola = get_object_or_404(Maqola, id=maqola_id)

    if request.method == 'POST':
        form = RoleSelectionForm(request.POST)
        if form.is_valid():
            selected_roles = form.cleaned_data['selected_roles']
            
            # Ushbu rollarga ega foydalanuvchilarni topamiz
            users_to_send = CustomUser.objects.filter(role__in=selected_roles)

            # Har bir foydalanuvchiga ariza yuborilganligini logga yozamiz
            for user in users_to_send:
                MaqolaYuborishLog.objects.create(maqola=maqola, kimga=user.role)

            messages.success(request, f"{len(users_to_send)} ta foydalanuvchiga ariza yuborildi.")
            return redirect('maqola_message')  # Yoki kerakli sahifaga
    else:
        form = RoleSelectionForm()

    return render(request, 'sendArticle.html', {'form': form, 'maqola': maqola})


@login_required
def roleMaqolaMessage(request):
    user_role = request.user.role  # foydalanuvchining roli
    yuborilgan_arizalar = MaqolaYuborishLog.objects.filter(kimga=user_role).order_by('maqola','-yuborilgan_vaqt').distinct('maqola')
    
    context = {
        'yuborilgan_arizalar': yuborilgan_arizalar
    }
    return render(request, 'roleMaqolaMessage.html', context)



from django.views.decorators.http import require_POST

@require_POST
@login_required
def maqola_javob_berish(request, log_id):
    maqola = get_object_or_404(MaqolaYuborishLog, id=log_id)

    if maqola.kimga != request.user.role:
        messages.error(request, "Siz bu arizaga javob bera olmaysiz.")
        return redirect('role_maqola_messages')

    javob = request.POST.get('javob')

    if javob == 'qabul':
        maqola.holat = True
    elif javob == 'rad':
        maqola.holat = False
    else:
        messages.error(request, "Noto‘g‘ri amal.")
        return redirect('role_maqola_messages')

    maqola.javob_berilgan = True
    maqola.save()

    messages.success(request, "Javob muvaffaqiyatli yuborildi.")
    return redirect('role_maqola_messages')

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch

@staff_member_required
def maqola_javoblar_admin(request):
    # Faqat javob berilgan arizalar
    loglar = MaqolaYuborishLog.objects.filter(javob_berilgan=True).select_related('maqola')

    # Vakansiya bo‘yicha guruhlab olish uchun dict tayyorlaymiz
    guruhlangan = {}

    for log in loglar:
        maqola_nomi = log.maqola.sarlavha
        if maqola_nomi not in guruhlangan:
            guruhlangan[maqola_nomi] = []
        guruhlangan[maqola_nomi].append(log)

    return render(request, 'admin_ariza_javoblar.html', {'guruhlangan': guruhlangan})

def javob_ochirish(request, pk):
    javob = get_object_or_404(MaqolaYuborishLog, pk=pk)
    if request.method == 'POST':
        javob.delete()
    return redirect('admin_maqola_jadval')  # yoki sizning ro‘yhat sahifangiz nomi