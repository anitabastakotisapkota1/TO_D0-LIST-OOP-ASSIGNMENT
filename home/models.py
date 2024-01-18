from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class register(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    class Meta:
        permissions = [
            ("add_choice", "email")
        ]

class event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    due_dates = models.DateField()
    day = models.IntegerField(null=True)
    month = models.CharField(max_length=100,null=True)
    activity = models.TextField(max_length=500,null=True)
    completed = models.BooleanField(default = False)

class CompletedModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    day = models.IntegerField(null=True)
    month = models.CharField(max_length=100,null=True)
    activity = models.TextField(max_length=500,null=True)
    