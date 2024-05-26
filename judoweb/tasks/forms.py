from django import forms
from .models import *


class PDFForm(forms.ModelForm):
    nombre = forms.CharField(max_length=200, required=True, label="Nombre")
    evento = forms.ModelChoiceField(
        queryset=Evento.objects.all(), required=True, label="Evento"
    )

    class Meta:
        model = PDF
        fields = ["archivo", "evento"]

    def clean_archivo(self):
        archivo = self.cleaned_data["archivo"]
        if not archivo.name.endswith(".pdf"):
            raise forms.ValidationError("El archivo debe ser un PDF.")
        return archivo


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ["titulo", "descripcion", "imagen"]


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ["nombre"]
