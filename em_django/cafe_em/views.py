from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)

from .models import Dish, Order, OrderItem


def index_view(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.prefetch_related("order_items__dish").all()
    return render(
        request,
        template_name="cafe_em/index.html",
        context={"orders": orders},
    )


class ToDoListIndexView(ListView):
    template_name = "cafe_em/index.html"
    queryset = Order.objects.all()[:3]
