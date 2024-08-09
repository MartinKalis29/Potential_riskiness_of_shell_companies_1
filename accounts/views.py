from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.models import Profile
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')


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
