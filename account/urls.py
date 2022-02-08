from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    # path('login/', views.user_login, name='login'),

    # path('register/', views.UserRegister.as_view(), name='register'),

    path('profil/', views.profil, name='profil'),

    path('edit_profil/', views.edit_profil, name='edit_profil'),

    path('change_password/', views.change_password, name='change_password'),

    path('user_logout/', views.user_logout, name='user_logout'),
]