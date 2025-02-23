from typing import Any, Dict, List, Optional
from rest_framework import serializers
from .models import Dish, Order, OrderItem


class DishSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Dish.
    Использует все поля модели.
    """

    class Meta:
        model = Dish
        fields = "__all__"

    def validate_price(
        self,
        value,
    ):
        if value < 0:
            raise serializers.ValidationError(
                "Цена не может быть отрицательной.",
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели OrderItem.
    """

    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "dish",
            "quantity",
        ]


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.
    """

    order_items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "table_number",
            "status",
            "total_price",
            "order_items",
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания заказа.
    """

    order_items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "table_number",
            "order_items",
        ]

    def create(self, validated_data: Dict[str, Any]) -> Order:
        """
        Создаёт экземпляр заказа вместе
        """
        order_items_data: List[Dict[str, Any]] = validated_data.pop(
            "order_items",
            [],
        )
        order: Order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            dish_id: int = item_data.pop("dish")
            dish_instance: Dish = Dish.objects.get(id=dish_id)
            OrderItem.objects.create(
                order=order,
                dish=dish_instance,
                **item_data,
            )

        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления заказа.
    """

    order_items = OrderItemSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = Order
        fields = [
            "table_number",
            "status",
            "order_items",
        ]

    def update(
        self,
        instance: Order,
        validated_data: Dict[str, Any],
    ) -> Order:
        """
        Обновляет существующий заказ и связанные с ним позиции заказа.
        """
        order_items_data: Optional[List[Dict[str, Any]]] = validated_data.pop(
            "order_items",
            None,
        )

        instance.table_number = validated_data.get(
            "table_number",
            instance.table_number,
        )
        instance.status = validated_data.get(
            "status",
            instance.status,
        )
        instance.save()

        if order_items_data is not None:
            instance.order_items.all().delete()

            for item_data in order_items_data:
                dish: Any = item_data.get("dish")
                if isinstance(dish, int):
                    item_data["dish"] = Dish.objects.get(id=dish)
                OrderItem.objects.create(
                    order=instance,
                    **item_data,
                )

        return instance
