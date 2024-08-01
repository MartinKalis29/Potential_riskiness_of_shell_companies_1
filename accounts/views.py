from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import CharField, Textarea, DateField
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.models import Profile


class SubmittableLoginView(LoginView):
    template_name = 'form.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('home')


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'employee_id_number', 'password1', 'password2']

    birth_date = DateField()
    employee_id_number = CharField(label='Employee ID Number', max_length=50)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = False
        result = super().save(commit)
        birth_date = self.cleaned_data['birth_date']
        employee_id_number = self.cleaned_data['employee_id_number']
        profile = Profile(birth_date=birth_date, employee_id_number=employee_id_number, user=result)
        if commit:
            profile.save()
        return result


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')
