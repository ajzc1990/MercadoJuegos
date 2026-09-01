from django import forms
from .models import Producto, Pregunta

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['categoria', 'titulo', 'descripcion', 'precio', 'stock', 'condicion', 'imagen']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: PlayStation 5 Slim 1TB Spider-Man Bundle'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'condicion': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto_pregunta']
        widgets = {
            'texto_pregunta': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Escribe tu pregunta al vendedor...'
            })
        }

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto_respuesta']
        widgets = {
            'texto_respuesta': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2, 
                'placeholder': 'Escribe tu respuesta...'
            })
        }