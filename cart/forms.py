from django import forms
from .models import CartItem

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial = 1)

    def __init__(self, *args, **kwargs):
        self.dish = kwargs.pop('dish', None)
        super().__init__(*args, **kwargs)

class UpdateCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


