from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path(
        'tiles/',
        views.TilesAPIView.as_view(),
        name=views.TilesAPIView.name
    )
]
