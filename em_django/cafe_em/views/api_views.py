from typing import Optional
from django.db.models import F, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.request import Request

from ..models import Dish, Order
from ..serializers import (
    DishSerializer,
    OrderCreateSerializer,
    OrderSerializer,
    OrderUpdateSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API ViewSet для работы с заказами.

    Может:
    - Фильтрация заказов по статусу.
    - Создание заказа.
    - Частичное обновление заказа.
    - Удаление заказа.
    - Подсчет общей выручки от оплаченных заказов.
    """

    queryset = Order.objects.all().order_by("-id")
    serializer_class = OrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ["table_number", "status",]

    @action(detail=False, methods=["get"], url_path=r"status/(?P<status>\w+)")
    def filter_by_status(
        self, request: Request, status: Optional[str] = None
    ) -> Response:
        """
        Фильтрует заказы по статусу.
        """
        orders = self.queryset.filter(status=status.upper())
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="create",)
    def create_order(self, request: Request,) -> Response:
        """
        Создает новый заказ на основе переданных данных.
        """
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                OrderSerializer(order).data, status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,)

    @action(detail=True, methods=["patch"], url_path="update")
    def partial_update_order(
        self, request: Request, pk: Optional[str] = None,
    ) -> Response:
        """
        Частично обновляет заказ.
        """
        # Выводим в консоль для отладки идентификатор обновляемого заказа
        print(f"Updating order with ID: {pk}")
        order = self.get_object()
        serializer = OrderUpdateSerializer(
            order, data=request.data, partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,)

    @action(detail=True, methods=["delete"], url_path="delete")
    def delete_order(
        self, request: Request, pk: Optional[str] = None
    ) -> Response:
        """
        Удаляет заказ.
        """
        order = self.get_object()
        order.delete()
        return Response(
            {"message": "Order deleted"}, status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=["get"], url_path="total",)
    def total_sum(self, request: Request) -> Response:
        """
        Вычисляет общую сумму всех оплаченных заказов.
        """
        total_sum: Optional[float] = (
            Order.objects.filter(status=Order.Status.PAID).aggregate(
                total=Sum(
                    F("order_items__quantity") * F("order_items__dish__price")
                )
            )["total"]
            or 0
        )
        return Response({"total_sum": total_sum})


class DishViewSet(viewsets.ModelViewSet):
    """
    API ViewSet для работы с блюдами.

    Предоставляет стандартные CRUD операции для объектов модели Dish.
    """

    queryset = Dish.objects.all().order_by("-id")
    serializer_class = DishSerializer
