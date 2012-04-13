from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template.response import TemplateResponse

def home(request):
    return TemplateResponse(request,'main/home.html')
