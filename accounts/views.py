from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.models import Profile
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse


# Definícia pohľadu pre domovskú stránku
def home(request):
    return render(request, 'home.html')

# Definícia pohľadu pre štatistiky
from django.shortcuts import render
from .models import Company  # Predpokladajme, že máte model Company


def statistics_view(request):
    # Získanie top 10 spoločností s najvyšším počtom zamestnancov
    top_10_health_insurance_debt = Company.objects.all().order_by('-health_insurance_debt')[:10]
    top_10_social_insurance_debt = Company.objects.all().order_by('-social_insurance_debt')[:10]
    top_10_tax_debt = Company.objects.all().order_by('-tax_debt')[:10]
    top_10_yoy_sales = Company.objects.all().order_by('-yoy_sales')[:10]
    top_10_employee_count = Company.objects.all().order_by('-employee_count')[:10]

    # Vrátiť šablónu s údajmi
    return render(request, 'top_10_employee_count.html', {'top_10_employee_count': top_10_employee_count})


class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(
        required=False,
        input_formats=['%d/%m/%Y'],  # Formát, ktorý očakávame pri vstupe
        widget=forms.DateInput(attrs={'type': 'text', 'placeholder': 'DD/MM/YYYY'})
    )
    employee_id_number = forms.CharField(label='Employee ID Number', max_length=50, required=False)
    personal_number = forms.CharField(label='Personal Number', max_length=50, required=False)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    @atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                birth_date=self.cleaned_data['birth_date'],
                employee_id_number=self.cleaned_data['employee_id_number'],
                personal_number=self.cleaned_data['personal_number']
            )
        return user

class SubmittableLoginView(LoginView):
    template_name = 'form.html'

class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('home')

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Registration successful.')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'There was a problem with your registration.')
        return self.render_to_response(self.get_context_data(form=form))

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Tu pridajte kód na spracovanie emailu (napr. uloženie do databázy)
        return HttpResponse("Thank you for subscribing!")
    return redirect('/')  # Alebo vráťte späť na hlavnú stránku

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')
