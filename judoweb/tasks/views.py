from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from .forms import PDFForm
from .models import Comment, Noticia
from .forms import CommentForm
from django.contrib.auth.decorators import permission_required
from .forms import NoticiaForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.core.paginator import Paginator



def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password don`t match'
        })

@login_required
def home(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.save()
            return redirect('home')
    else:
        form = NoticiaForm()
    noticias = Noticia.objects.all()
    return render(request, 'home.html', {'form': form, 'noticias': noticias})

@user_passes_test(lambda u: u.is_superuser)
def delete_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    if request.method == 'POST':
        noticia.delete()
        return redirect('home')  
    return render(request, 'home.html', {'noticias': Noticia.objects.all()})


@user_passes_test(lambda u: u.is_superuser)
def edit_noticia(request):
    noticia = get_object_or_404(Noticia, pk=request.POST['id'])

    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('home')    
    else:
        form = NoticiaForm(instance=noticia)
    
    return render(request, 'home.html', {'form': form})



@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
        request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('home')        


@login_required
def calendar_view(request):
    comments = Comment.objects.all()
    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.save()
        return redirect('calendar')
    return render(request, 'calendar.html', {'comments': comments, 'form': form})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        if comment.user == request.user:
            comment.delete()
            return redirect('calendar')
    return redirect('calendar')  

@permission_required('judoweb.message_permissions')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user.has_perm('your_app.delete_any_comment'):
        comment.delete()
    elif comment.user == request.user:
        comment.delete()
    else:
        redirect('calendar')
    return redirect('calendar')


@login_required
def uploadpdf(request):    
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.user = request.user 
            pdf.save()
            return render(request, 'uploadpdf.html', {
                'form': PDFForm(),
                'message': "PDF has been successfully uploaded."
            })
    else:
        form = PDFForm()
    return render(request, 'uploadpdf.html', {
        'form': form,
    })

@user_passes_test(lambda u: u.is_superuser)
def pdf_list(request):
    pdfs = PDF.objects.all()
    paginator = Paginator(pdfs, 10) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)  
    return render(request, 'pdf_list.html', {'page_obj': page_obj})


