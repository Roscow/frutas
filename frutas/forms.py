
from django import forms
from .models import Fruta


class create_fruta(forms.ModelForm):
    class Meta:
        model = Fruta
        fields = ('nombre','descripcion','imagen'  )
        labels = {'imagen':'url de la imagen'}
        widgets={
            'nombre': forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'required':''
                }
            ),
            'descripcion': forms.Textarea(
                attrs ={
                    'class':'form-control'
                }
            ),
            'imagen': forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'https://images.unsplash.com/photo-1515778767554-42d4...',
                    'required':''
                }
            ),
        } 


