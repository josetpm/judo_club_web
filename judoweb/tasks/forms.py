from django import forms
from .models import *
from django import forms
from .models import Comment


class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        exclude = ['estado'] 
        fields = ['archivo', 'estado']

    def clean_archivo(self):
        archivo = self.cleaned_data['archivo']
        if not archivo.name.endswith('.pdf'):
            raise forms.ValidationError('Field must be PDF.')
        return archivo


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'descripcion', 'imagen']


