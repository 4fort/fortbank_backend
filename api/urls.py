from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('users/', views.getUsers),
    path('users/<int:id>', views.getUserInfo),

    path('users/<int:id>/updatebalance', views.updateBalance),

    path('tickets/', views.getTickets),
    path('tickets/<int:reference_id>', views.getTicket, name='get_ticket'),

    path('users/account/<int:id>', views.getUserAccount),
    path('users`/profile/<int:id>', views.getUserProfile),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
