from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register', views.register, name='register'),
    path('edit', views.edit, name='profile_edit'),
    path('profiles/<str:username>', views.profile, name='profile'),
    path('profiles/<str:username>/report', views.report, name='report')
]
