from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from viewer.views import home, statistics_view, companies, about_us, company_detail, search, \
    top_10_yoy_sales_view, top_10_tax_debt_view, top_10_social_insurance_debt_view, top_10_health_insurance_debt_view, \
    top_10_employee_count_view, ExecutiveFormView, CompanyFormView, privacy_policy, terms_of_service
from accounts.views import SubmittableLoginView, SubmittablePasswordChangeView, SignUpView, subscribe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('database/', companies, name='database'),
    path('statistics/', statistics_view, name='statistics'),
    path('about_us/', about_us, name='about_us'),
    path('company/create/', CompanyFormView.as_view(), name='company_create'),
    path('company/<int:company_id>/', company_detail, name='company_detail'),
    path('subscribe/', subscribe, name='subscribe'),  # Pridajte lomku na koniec
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-of-service/', terms_of_service, name='terms_of_service'),
    path('executive/create/', ExecutiveFormView.as_view(), name='executive_create'),

    # Authentication
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Search and Top 10 Views
    path('search/', search, name='search'),
    path('top-10-yoy-sales/', top_10_yoy_sales_view, name='top_10_yoy_sales'),
    path('top-10-tax-debt/', top_10_tax_debt_view, name='top_10_tax_debt'),
    path('top-10-social-insurance-debt/', top_10_social_insurance_debt_view, name='top_10_social_insurance_debt'),
    path('top-10-health-insurance-debt/', top_10_health_insurance_debt_view, name='top_10_health_insurance_debt'),
    path('top-10-employee-count/', top_10_employee_count_view, name='top_10_employee_count'),
]
