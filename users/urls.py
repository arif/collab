from django.urls import path

from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('login-as/', views.LoginAsView.as_view(), name='login-as'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh-token'),
    path('me/', views.VerifyTokenView.as_view(), name='verify-token'),
]
