"""
URL configuration for judoweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from tasks.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("home/", home, name="home"),
    path("signup/", signup, name="signup"),
    path("calendar/", calendar_view, name="calendar"),
    path("delete_comment/<int:comment_id>/", delete_comment, name="delete_comment"),
    path("logout/", signout, name="logout"),
    path("signin/", signin, name="signin"),
    path("uploadpdf/", uploadpdf, name="uploadpdf"),
    path("delete/<int:noticia_id>/", delete_noticia, name="delete_noticia"),
    path("edit/", edit_noticia, name="edit_noticia"),
    path("pdf-list/", pdf_list, name="pdf_list"),
    path("cambiar_estado_pdf/", cambiar_estado_pdf, name="cambiar_estado_pdf"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
