from django.urls import path

from . import views


urlpatterns = [
    path('list/', views.GameListAPIView.as_view(), name='game_list'),
]
