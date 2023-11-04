from django.urls import include, path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path(
        'filters/',
        views.FilterAPIView.as_view(),
        name=views.FilterAPIView.name
    )
]
