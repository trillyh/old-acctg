from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def say_hello(request):
    return HttpResponse('Hello world')

def send_html(request):
    return render(request, 'hello.html')



