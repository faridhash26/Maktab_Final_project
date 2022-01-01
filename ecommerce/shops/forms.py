from django.forms import ModelForm, Textarea, TextInput
from .models import Shop


class CreateShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = ('shop_type', 'name', 'address')
        widgets = {
            'name': TextInput(attrs={'class':'w3-input w3-border'}),
            'shop_type': TextInput(attrs={'class':'w3-input w3-border'}),
            'address': Textarea(attrs={'class':"w3-input w3-padding-16 w3-border"}),
        }

  