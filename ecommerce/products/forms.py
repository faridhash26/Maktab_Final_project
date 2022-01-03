from django.forms import ModelForm, CheckboxSelectMultiple, TextInput,NumberInput,CheckboxInput,FileInput,SelectMultiple
from .models import Product


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'price','weight','stock', 'is_published','tag','category')
        widgets = {
            'name': TextInput(attrs={'class':'w3-input w3-border'}),
            'image': FileInput(attrs={'class':'w3-input w3-border'}),
            'price': NumberInput(attrs={'class':"w3-input w3-padding-16 w3-border"}),
            'weight': NumberInput(attrs={'class':'w3-input w3-border'}),
            'stock': NumberInput(attrs={'class':'w3-input w3-border'}),
            'is_published': CheckboxInput(),
            "tag":SelectMultiple(),
            "category":SelectMultiple(),
        }
