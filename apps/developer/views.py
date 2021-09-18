from django.shortcuts import render

def index_developer(request):
    return render(request,'developer/index_developer.html')

def auth(request):
    return render(request,'user/auth.html')