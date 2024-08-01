from django.contrib import admin
from django.urls import path
from viewer.views import companies, home, about_us, statistics, company_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('database/', companies, name='database'),
    path('statistics/', statistics, name='statistics'),
    path('about_us/', about_us, name='about_us'),
    path('company/<int:company_id>/', company_detail, name='company_detail'),
    path('companies/', companies, name='companies'),
]
