from django.contrib import admin
from .models import *

arrayModels = [PDF, Noticia, Comment, Evento]

admin.site.register(arrayModels)
