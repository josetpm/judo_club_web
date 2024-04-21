from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import datetime as dt
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from django.http import HttpResponse
from google.oauth2 import service_account
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from django.db import models
import datetime
import pytz


SCOPES = ["https://www.googleapis.com/auth/calendar"]

class Event(models.Model):
    summary = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.summary

def home(request):
    return render(request, 'home.html')


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
def calendar_view(request, month=None, year=None):
    if month and year:
        # Genera el rango de fechas para el mes y año especificados
        first_day = datetime.date(year, month, 1)
        last_day = datetime.date(year, month, 1) + datetime.timedelta(days=32)
        last_day = last_day - datetime.timedelta(days=last_day.day)
    else:
        # Si no se especifican, usa el mes y año actuales
        today = datetime.date.today()
        first_day = today.replace(day=1)
        last_day = (today + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

    # Autenticación y recuperación de eventos como antes
    try:
        creds = Credentials.from_authorized_user_file('client_secret.json')
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events_data = events_result.get('items', [])

        for event_data in events_data:
            start_time = event_data['start'].get('dateTime', event_data['start'].get('date'))
            end_time = event_data['end'].get('dateTime', event_data['end'].get('date'))
            start_time = datetime.datetime.fromisoformat(start_time)
            end_time = datetime.datetime.fromisoformat(end_time)
            start_time = pytz.utc.localize(start_time)
            end_time = pytz.utc.localize(end_time)
            Event.objects.create(summary=event_data.get('summary', ''), start_time=start_time, end_time=end_time)

        events = Event.objects.filter(start_time__range=(first_day, last_day))
        context = {'month': month, 'year': year, 'days': range(1, last_day.day + 1), 'events': events}
        return render(request, 'calendar.html', context)

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")

class GoogleCalendarManager:
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        # Carga las credenciales del archivo JSON
        creds = service_account.Credentials.from_service_account_file(
            'credencials.json', scopes=SCOPES)

        # Construye el servicio de Google Calendar
        return build('calendar', 'v3', credentials=creds)

    def list_events(self, start_date, end_date):
        events_result = self.service.events().list(calendarId='primary', timeMin=start_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

calendar = GoogleCalendarManager()











