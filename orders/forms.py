from django import forms
from django.utils.html import strip_tags
from phonenumber_field.formfields import PhoneNumberField


class OrderForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Имя'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Фамилия'
        })
    )
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Номер телефона',
            'readonly': 'readonly'
        })
    )
    address1 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black pr-10',
            'placeholder': 'Адрес 1'
        })
    )
    address2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Адрес 2 (опционально)'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Город'
        })
    )
    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Страна'
        })
    )
    postal_code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Почтовый индекс'
        })
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['phone'].initial = user.phone
            self.fields['address1'].initial = user.address1
            self.fields['address2'].initial = user.address2
            self.fields['city'].initial = user.city
            self.fields['country'].initial = user.country
            self.fields['postal_code'].initial = user.postal_code


    def clean(self):
        cleaned_data = super().clean()
        for field in ['address1', 'address2', 'city', 
                      'country', 'postal_code', 'phone']:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])
        return cleaned_data
    