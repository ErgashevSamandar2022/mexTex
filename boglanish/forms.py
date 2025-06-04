from django import forms
from .models import Maqola,Contact,NewMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


class MaqolaForm(forms.ModelForm):
    class Meta:
        model = Maqola
        fields = ['sarlavha', 'muallif', 'matn', 'kategoriya', 'kalit_sozlar', 'telefon_raqam', 'fayl']
        widgets = {
            'matn': forms.Textarea(attrs={'rows': 10}),
        }
       
class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label='Xabar matni')



ROLES = (
        ('user', 'Foydalanuvchi'),
        ('taqrizchi_inf1', 'Jo\'rayev Adhamjon Informatika Taqrizchisi 1-raqamli'),
        ('taqrizchi_inf2', 'Sobirov Azizber Informatika Taqrizchisi 2-raqamli'),
        ('taqrizchi_inf3', 'Xasanov Saredor Informatika Taqrizchisi 3-raqamli'),
        ('taqrizchi_iq1', 'Ergasheva Halima Iqtisod Taqrizchisi 1-raqamli'),
        ('taqrizchi_iq2', 'Muhammadaliyev Zuhriddin Iqtisod Taqrizchisi 2-raqamli'),
        ('admin', 'Administrator'),
    )
    
class RoleSelectionForm(forms.Form):
    selected_roles = forms.MultipleChoiceField(
        choices=ROLES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Kimlarga yuborilsin?"
    )