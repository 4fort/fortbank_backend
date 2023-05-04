from django.urls import path
from . import views

urlpatterns = [
    path('fortbank/admin/', views.getAdmin),
    path('users/', views.getUsers),
    path('users/<int:id>', views.getUserInfo),
]