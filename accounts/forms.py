#forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'role')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agar oddiy foydalanuvchi ro'yxatdan o'tayotgan bo'lsa, role maydonini olib tashlash
        if not self.initial.get('is_superuser'):
            self.fields.pop('role', None)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if not hasattr(user, 'role'):  # Agar role tanlanmagan bo'lsa
            user.role = 'user'  # Standart rol
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'is_staff', 'is_superuser')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Faqat adminlar uchun role va boshqa muhim maydonlarni ko'rsatish
        if not self.instance.is_superuser:
            self.fields.pop('is_superuser', None)
            self.fields.pop('is_staff', None)
            self.fields.pop('user_permissions', None)
            self.fields.pop('groups', None)