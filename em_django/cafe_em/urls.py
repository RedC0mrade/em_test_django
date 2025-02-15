from django.urls import path

from . import views

app_name = "cafe_em"

urlpatterns = [
    path("", views.index_view, name="index"),
]
