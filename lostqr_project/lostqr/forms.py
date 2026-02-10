from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'username',
            'mail',
            'phone',
            'social_media',
            'message',
        ]

        labels = {
            'username': 'İsim (Gerekli)',
            'mail': 'E-posta Adresi',
            'phone': 'Telefon Numarası',
            'social_media': 'Sosyal Medya (Örn: instagram: kullanıcıadı)',
            'message': 'Bulan kişiye mesajınız (Gerekli)',
        }

    def clean(self):
        cleaned_data = super().clean()
        mail = cleaned_data.get('mail')
        phone = cleaned_data.get('phone')
        social_media = cleaned_data.get("social_media")

        filled_count = sum(bool(x) for x in [mail, phone, social_media])
        if filled_count < 1:
            raise forms.ValidationError(
                'En az bir iletişim bilgisi (Email, Telefon veya Sosyal Medya) doldurmalısınız.'
            )
        return cleaned_data