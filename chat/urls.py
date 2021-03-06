from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:chat_id>', views.detail, name='detail'),
    path('create', views.create, name='create')
]
