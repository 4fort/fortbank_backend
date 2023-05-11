from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager


# class User(models.Model):
#     owner_name = models.CharField(max_length=200)
#     email = models.CharField(max_length=200)
#     card_num = models.IntegerField(unique=True)
#     card_pin = models.IntegerField()
#     balance = models.FloatField(default=0)

#     def __str__(self):
#         return self.owner_name + ' (' + str(self.card_num) + ') P' + str(self.balance)


# class Admin(models.Model):
#     username = models.CharField(max_length=150)
#     password = models.CharField(max_length=150)

class AccountManager(BaseUserManager):

    def create_user(self, owner_name, email, card_num, card_pin, balance, **other_fields):
        if not owner_name:
            raise ValueError('You must provide a name!')
        if not email:
            raise ValueError('You must provide an email!')

        email = self.normalize_email(email)
        user = self.model(
            owner_name=owner_name,
            email=email,
            card_num=card_num,
            card_pin=card_pin,
            balance=balance,
            **other_fields
        )
        user.save()
        return user

    def create_superuser(self, email, owner_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, owner_name, password, **other_fields)


class UserAccount(AbstractUser, PermissionsMixin):
    owner_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    card_num = models.PositiveIntegerField(unique=True)
    card_pin = models.PositiveIntegerField()
    balance = models.FloatField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField()

    objects = AccountManager()

    USERNAME_FIELD = 'card_num'
    REQUIRED_FIELDS = ['owner_name', 'email']

    def get_username(self):
        return str(self.card_num)

    def get_full_name(self):
        return self.owner_name

    def __str__(self):
        return self.owner_name

    class Meta:
        ordering = ['id']
