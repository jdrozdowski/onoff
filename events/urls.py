from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('past/', views.past, name='past'),
    path('mine/', views.mine, name='mine'),
    path('mine/past/', views.mine_past, name='mine_past'),
    path('<int:event_id>', views.detail, name='detail'),
    path('create', views.create, name='create'),
    path('<int:event_id>/edit', views.edit, name='edit'),
    path('<int:event_id>/delete', views.delete, name='delete'),
    path('<int:event_id>/join', views.join, name='join'),
    path('<int:event_id>/leave', views.leave, name='leave'),
    path('<int:event_id>/promote', views.promote_to_organizer, name='promote'),
]
