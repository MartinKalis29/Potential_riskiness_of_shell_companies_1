from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    personal_id_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
