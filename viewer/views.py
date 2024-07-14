from django.http import HttpResponse
from django.shortcuts import render

from viewer.models import Company


# Create your views here.
def companies(request):
    result = Company.objects.all()
    context = {'companies': result}
    return render(
        request,
        'database.html',
        context
    )


def home(request):
    return render(request, 'home.html', {'title': 'Welcome to SafeBusiness'})


def about_us(request):
    return render(request, 'about_us.html', {'title': 'Welcome to SafeBusiness'})