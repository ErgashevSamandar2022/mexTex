from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'nashr_yili', 'nashr_soni', 'num', 'num1', 'image', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jurnal sarlavhasi'}),
            'nashr_yili': forms.NumberInput(attrs={'class': 'form-control'}),
            'nashr_soni': forms.NumberInput(attrs={'class': 'form-control'}),
            'num': forms.NumberInput(attrs={'class': 'form-control'}),
            'num1': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
