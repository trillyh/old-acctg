from django.shortcuts import render
from django.http import HttpResponse
from .models import JournalEntry
# Create your views here.

def show_welcome_page(request):
    return render(request, "accounting/index.html")

def send_html(request):
    return render(request, 'hello.html')

def latest_entries(request):
    return render(request, "accounting/playground.html") 
