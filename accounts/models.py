from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, CASCADE, DateField, CharField


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    birth_date = DateField(null=True, blank=True)
    employee_id_number = CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user}"
