from django.db import models
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    owner_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    card_num = models.IntegerField(unique=True)
    card_pin = models.IntegerField()
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.owner_name + ' (' + str(self.card_num) + ') P' + str(self.balance)
    
class Admin(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)