from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from cafe_em.views import api_views, web_views


app_name = "cafe_em"

handler404 = "cafe_em.views.custom_404_view"

schema_view = get_schema_view(
    openapi.Info(
        title="Cafe_em",
        default_version="v1",
        description="Документация API для проекта Cafe_em",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(
    r"orders",
    api_views.OrderViewSet,
    basename="order",
)
router.register(
    r"dish",
    api_views.DishViewSet,
    basename="dish",
)

urlpatterns = [
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(
        "",
        web_views.OrderListView.as_view(),
        name="order_list",
    ),
    path(
        "dishs/",
        web_views.DishListView.as_view(),
        name="dish_list",
    ),
    path(
        "order/<int:pk>/",
        web_views.OrderDetailView.as_view(),
        name="order_detail",
    ),
    path(
        "dish/<int:pk>/",
        web_views.DishDetailView.as_view(),
        name="dish_detail",
    ),
    path(
        "new_order",
        web_views.OrderCreateView.as_view(),
        name="order_form",
    ),
    path(
        "new_dish",
        web_views.DishCreateView.as_view(),
        name="dish_form",
    ),
    path(
        "<int:pk>/order_update",
        web_views.OrderUpdateView.as_view(),
        name="order_update_form",
    ),
    path(
        "<int:pk>/order_delete",
        web_views.OrderDeleteView.as_view(),
        name="order_delete",
    ),
    path(
        "total_sum",
        web_views.OrderTotalSumView.as_view(),
        name="total_sum",
    ),
    path(
        "api/",
        include(router.urls),
    ),
]
