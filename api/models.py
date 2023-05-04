from django.db import models

class User(models.Model):
    owner_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    card_num = models.IntegerField()
    card_pin = models.IntegerField()
    balance = models.FloatField()

    def __str__(self):
        return self.owner_name + ' (' + str(self.card_num) + ') P' + str(self.balance)
    
class Admin(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)