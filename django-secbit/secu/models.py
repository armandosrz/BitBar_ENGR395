from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    hashed_password = models.CharField(max_length=200)
    salt = models.CharField(max_length=200)
    profile = models.CharField(max_length=100, null=True)
    bitbars = models.IntegerField(default=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
