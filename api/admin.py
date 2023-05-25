from django.contrib import admin
from .models import UserAccount, UserProfile, TransactionTicket

admin.site.register(UserAccount)
admin.site.register(UserProfile)
admin.site.register(TransactionTicket)
