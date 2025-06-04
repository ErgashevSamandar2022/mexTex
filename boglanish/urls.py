from django.urls import path
from .views import (
    ContactPagesViews,
    journal_message,
    boglanish,
    maqola_yuborish,
    maqolalar_royxati,
    inbox,
    contactMessage,
    maqola_tasdiqlash,
    maqola_rad_etish,
    maqola_send_taqriz,
    roleMaqolaMessage,
    maqola_javob_berish,
    maqola_javoblar_admin,
    javob_ochirish
)

urlpatterns = [
    # Contact (bog‘lanish) sahifalari
    path("contact/", ContactPagesViews.as_view(), name="boglanish"),  # Form sahifasi
    path('boglanish/', boglanish, name='boglanish'),
    # path('maqolalar/', MaqolaListView.as_view(), name='maqolalar'),  # ro'yxat uchun
    path('maqola-yuborish/', maqola_yuborish, name='maqola_yuborish'),
    path('maqola-royhati/', maqolalar_royxati, name='maqola_message'),
    path('journal/messages/', journal_message, name='journal_message'),
    path('xabarlar/', inbox, name='inbox'),
    path('contactMessage/', contactMessage, name='contactMess'),
    path('maqola/<int:maqola_id>/tasdiqlash/', maqola_tasdiqlash, name='maqola_tasdiqlash'),
    path('maqola/<int:maqola_id>/rad_etish/', maqola_rad_etish, name='maqola_rad_etish'),

    path('maqola/<int:maqola_id>/send/', maqola_send_taqriz, name='send_taqriz'),
    path('role-maqola-messages/', roleMaqolaMessage, name='role_maqola_messages'),
    path('maqola_javob/<int:log_id>/', maqola_javob_berish, name='maqola_javob_berish'),
    path('admin/maqola-jadval/', maqola_javoblar_admin, name='admin_maqola_jadval'),
    path('javob/<int:pk>/ochirish/', javob_ochirish, name='javob_ochirish'),
]