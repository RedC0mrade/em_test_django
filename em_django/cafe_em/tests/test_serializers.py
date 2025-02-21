import pytest
from cafe_em.serializers import (
    DishSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from cafe_em.models import Order, Dish, OrderItem


@pytest.mark.django_db
def test_dish_serializer_valid():
    dish = Dish.objects.create(
        name="Борщ",
        price=10.00,
    )
    serializer = DishSerializer(dish)

    expected_data = {
        "id": dish.id,
        "name": "Борщ",
        "price": "10.00",
    }
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_dish_serializer_invalid_price():
    serializer = DishSerializer(
        data={
            "name": "Борщ",
            "price": -10.00,
        }
    )
    assert not serializer.is_valid()
    assert "price" in serializer.errors


@pytest.mark.django_db
def test_order_serializer_valid():
    dish = Dish.objects.create(
        name="Борщ",
        price=10.00,
    )
    order = Order.objects.create(
        table_number=1,
        status="waiting",
    )
    order_item = OrderItem.objects.create(
        order=order,
        dish=dish,
        quantity=2,
    )

    serializer = OrderSerializer(order)

    expected_data = {
        "id": order.id,
        "table_number": 1,
        "status": "waiting",
        "order_items": [
            {
                "id": order_item.id,
                "dish": dish.id,
                "quantity": 2,
            }
        ],
        "total_price": 20.00,
    }

    assert serializer.data == expected_data


@pytest.mark.django_db
def test_order_serializer_invalid_status():
    # Создаем заказ с неправильным статусом
    order = Order.objects.create(table_number=1, status="invalid_status",)

    # Сериализуем заказ
    serializer = OrderSerializer(order)

    # Проверяем, что валидация не пройдет, и будут ошибки
    assert not serializer.is_valid()
    assert "status" in serializer.errors


@pytest.mark.django_db
def test_order_item_serializer_valid():
    dish = Dish.objects.create(name="Борщ", price=10.00)
    order = Order.objects.create(table_number=1, status="waiting")

    order_item = OrderItem.objects.create(order=order, dish=dish, quantity=2)

    serializer = OrderItemSerializer(order_item)
    expected_data = {
        "id": order_item.id,
        "dish": dish.id,
        "quantity": 2,
    }
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_order_item_serializer_invalid_quantity():
    # Создаем блюдо и заказ
    dish = Dish.objects.create(name="Борщ", price=10.00)
    order = Order.objects.create(table_number=1, status="waiting")

    # Пытаемся создать OrderItem с некорректным количеством
    # order_item = OrderItem(order=order, dish=dish, quantity=-1,)

    # Сериализуем OrderItem
    serializer = OrderItemSerializer(data={"order"=order, "dish"=dish, "quantity"=-1,},)

    # Проверяем, что валидация не пройдет, и будут ошибки
    assert not serializer.is_valid()
    assert "quantity" in serializer.errors
