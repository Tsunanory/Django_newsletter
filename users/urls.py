from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, email_verification, UserResetPasswordView, UserListView, BlockUserView, \
    BlockUserConfirmView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='registration'),
    path('reset_password/', UserResetPasswordView.as_view(), name='reset_password'),
    path('email_confirmation/<str:token>/', email_verification, name='email_confirmation'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('block_user/<int:pk>/', BlockUserView.as_view(), name='block_user'),
    path('block_user_confirm/<int:pk>/', BlockUserConfirmView.as_view(), name='block_user_confirm'),
]
