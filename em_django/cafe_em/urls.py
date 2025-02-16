from django.urls import path

from . import views

app_name = "cafe_em"

urlpatterns = [
    path(
        "",
        views.OrderListView.as_view(),
        name="order_list",
    ),
    path(
        "dishs/",
        views.DishListView.as_view(),
        name="dish_list",
    ),
    path(
        "order/<int:pk>/",
        views.OrderDetailView.as_view(),
        name="order_detail",
    ),
    path(
        "dish/<int:pk>/",
        views.DishDetailView.as_view(),
        name="dish_detail",
    ),
    path(
        "new_order",
        views.OrderCreateView.as_view(),
        name="order_form",
    ),
    path(
        "new_dish",
        views.DishCreateView.as_view(),
        name="dish_form",
    ),
]
