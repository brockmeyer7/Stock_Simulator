from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    cash = models.DecimalField(default=10000, decimal_places=2, max_digits=10)

class Owned(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(blank=False, max_length=5)
    shares = models.IntegerField(blank=False)

class Transactions(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(blank=False, max_length=5)
    price = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    shares = models.IntegerField(blank=False)
    type = models.CharField(blank=False, max_length=5)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False)