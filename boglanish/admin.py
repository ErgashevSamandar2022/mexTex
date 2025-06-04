from django.contrib import admin
from .models import Contact, NewMessage, Maqola

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')

admin.site.register(Contact, ContactAdmin)

@admin.register(NewMessage)
class NewMessageadmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'message', 'created_at')
    
@admin.register(Maqola)
class MaqolaMessageAdmin(admin.ModelAdmin):
    list_display = ('sarlavha', 'muallif', 'matn', 'kategoriya','kalit_sozlar','telefon_raqam','fayl','yaratilgan_sana')