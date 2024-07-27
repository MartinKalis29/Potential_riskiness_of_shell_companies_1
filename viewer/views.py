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
    return render(request, 'about_us.html', {'title': 'About our website'})


def statistics(request):
    return render(request, 'statistics.html', {'title': 'Statistics'})


def company(request, pk):
    if Company.objects.filter(id=pk).exists():
        result = Company.objects.get(id=pk)
        return render(request, 'company.html', {'title': result.name, 'company': result})
    result = Company.objects.all().order_by('name')
    return render(request, 'database.html', {'title': 'Database', 'database': result})
