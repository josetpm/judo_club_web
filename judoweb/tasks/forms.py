from django import forms
from .models import PDF, Noticia

class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['archivo']

    def clean_archivo(self):
        archivo = self.cleaned_data['archivo']
        if not archivo.name.endswith('.pdf'):
            raise forms.ValidationError('Field must be PDF.')
        return archivo


from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'descripcion', 'imagen']