from django.db import models

class PDF(models.Model):
    archivo = models.FileField(upload_to='pdfs/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.archivo.name
