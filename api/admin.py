from django.contrib import admin
from .models import UserWallet, UserAccount, UserProfile, TransactionTicket

admin.site.register(UserWallet)
admin.site.register(UserAccount)
admin.site.register(UserProfile)
admin.site.register(TransactionTicket)
