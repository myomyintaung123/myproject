#from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required(login_url='/users/login/')
def home(request):
    #return HttpResponse("Hello home page")
    return render(request, 'home.html')

@login_required(login_url='/users/login/')
def about(request):
    #return HttpResponse("Hello about page")
    return render(request, 'about.html')