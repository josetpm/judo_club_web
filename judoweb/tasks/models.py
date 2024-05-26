from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="noticias/")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_publicacion"]

    def __str__(self):
        return self.titulo


class Evento(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class PDF(models.Model):
    archivo = models.FileField(upload_to="pdfs/")
    fecha_subida = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, default=None)

    estado = models.CharField(
        max_length=50,
        default="pendiente",
        choices=[
            ("pagado", "Pagado"),
            ("pendiente", "Pendiente"),
            ("rechazado", "Rechazado"),
        ],
    )

    def __str__(self):
        return self.archivo.name
