from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import RegisterView, verification, CheckEmail, UserDetailView, change_password

app_name = 'users'


urlpatterns = [
    path('login', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('verify/<int:user_pk>/<verification_code>/', verification, name='verification'),
    path('checkemail', CheckEmail.as_view(), name='checkemail'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user'),
    path('user/change_password/<int:user_pk>', change_password, name='change_password'),
]
