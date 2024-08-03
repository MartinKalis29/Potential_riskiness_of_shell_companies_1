from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

from accounts.views import SubmittableLoginView, SubmittablePasswordChangeView, SignUpView
from viewer.views import companies, home, about_us, statistics, company_detail, search, statistics_view, \
    top_10_yoy_sales_view, top_10_tax_debt_view, top_10_social_insurance_debt_view, top_10_health_insurance_debt_view, \
    top_10_employee_count_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('database/', companies, name='database'),  # upravená cesta, ktorá teraz obsahuje kód zo šablóny companies
    path('statistics/', statistics, name='statistics'),
    path('about_us/', about_us, name='about_us'),
    path('company/<int:company_id>/', company_detail, name='company_detail'),  # cesta pre company_detail

    # authentication
    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('search/', search, name='search'),

    path('statistics/', statistics_view, name='statistics'),
    path('top-10-yoy-sales/', top_10_yoy_sales_view, name='top_10_yoy_sales'),
    path('top-10-tax-debt/', top_10_tax_debt_view, name='top_10_tax_debt'),
    path('top-10-social-insurance-debt/', top_10_social_insurance_debt_view, name='top_10_social_insurance_debt'),
    path('top-10-health-insurance-debt/', top_10_health_insurance_debt_view, name='top_10_health_insurance_debt'),
    path('top-10-employee-count/', top_10_employee_count_view, name='top_10_employee_count'),
]
