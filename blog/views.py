from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, "blog/home.html", {"team":"Welcome to djangoBlog"})

def about(request):
    return render(request, "blog/about.html", {"team": "Us"})

def contact(request):
    return render(request, "blog/contact.html", {"team": "Us"})