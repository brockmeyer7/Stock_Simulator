from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    cash = models.FloatField(blank=False, default=10000)

class Owned(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(blank=False, max_length=5)
    shares = models.IntegerField(blank=False)

class Transactions(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(blank=False, max_length=5)
    price = models.FloatField(blank=False)
    shares = models.IntegerField(blank=False)
    type = models.CharField(blank=False, max_length=5)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False)