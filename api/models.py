from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    card_num = models.PositiveIntegerField(null=True)
    card_pin = models.PositiveIntegerField(null=True)
    balance = models.FloatField(null=True)

    def __str__(self):
        return self.user.username


class FortBank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    owner_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    card_num = models.IntegerField(null=True)
    card_pin = models.IntegerField(null=True)
    balance = models.FloatField(null=True)

    def __str__(self):
        return self.owner_name + ' (' + str(self.card_num) + ') P' + str(self.balance)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    mobile_number = models.PositiveBigIntegerField(null=True)

    MALE = 1
    FEMALE = 2
    OTHER = 3
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, null=True)

    SINGLE = 1
    MARRIED = 2
    WIDOWED = 3
    DIVORCED = 4
    CIVIL_STATUS_CHOICES = (
        (SINGLE, 'Single'),
        (MARRIED, 'Married'),
        (WIDOWED, 'Widowed'),
        (DIVORCED, 'Divorced'),
    )
    civil_status = models.PositiveSmallIntegerField(
        choices=CIVIL_STATUS_CHOICES, null=True)

    birthdate = models.DateField(null=True)
    address = models.CharField(null=True, max_length=500)

    def __str__(self):
        return self.user.username


class TransactionTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reference_id = models.PositiveIntegerField(unique=True, null=True)

    def save(self, *args, **kwargs):
        current_date = datetime.now()
        day_of_year = current_date.timetuple().tm_yday
        seconds = current_date.strftime("%S")

        self.reference_id = int(
            str(self.user.id) + str(day_of_year) + str(seconds))

        super().save(*args, **kwargs)


class UserContacts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='contacts', null=True)
    contact = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='contact_of', null=True)


class UserTransactions(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    )

    sender = models.ForeignKey(
        User, related_name='sent_transactions', on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(
        User, related_name='received_transactions', on_delete=models.SET_NULL, null=True)
    transaction_date = models.DateField(auto_now_add=True)
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f"{self.transaction_date} - {self.transaction_type}: {self.amount}"
