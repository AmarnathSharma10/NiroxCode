from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    age = models.PositiveIntegerField(default=12)
    email=models.CharField(null=True, blank=True,max_length=40)

    def __str__(self):
        return self.user.username
