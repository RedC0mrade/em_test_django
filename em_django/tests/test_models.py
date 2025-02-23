from django.forms import ValidationError
import pytest
from cafe_em.models import Dish, Order, OrderItem


def test_create_dish(dish):
    assert dish.name == "Борщ"
    assert dish.price == 3.5


def test_create_order(order):
    assert order.table_number == 1
    assert order.status == "waiting"


def test_create_order_item(order_item):
    assert order_item.quantity == 2
    assert order_item.dish.name == "Борщ"


def test_order_total_price(order_item):
    order = order_item.order
    assert order.total_price() == 7.0


def test_unique_order_item(dish, order):
    OrderItem.objects.create(
        order=order,
        dish=dish,
        quantity=2,
    )
    with pytest.raises(Exception):
        OrderItem.objects.create(
            order=order,
            dish=dish,
            quantity=3,
        )


def test_delete_order_item(order_item):
    order = order_item.order
    order_item.delete()
    assert order.order_items.count() == 0


def test_update_order_status(order):
    # Изменение статуса заказа
    order.status = "paid"
    order.save()
    order.refresh_from_db()
    assert order.status == "paid"


def test_order_with_invalid_status(order):
    # Проверка, что нельзя присвоить заказу недопустимый статус
    invalid_status = "invalid_status"
    order.status = invalid_status
    with pytest.raises(ValidationError):  # Ожидаем ошибку валидации
        order.save()


def test_order_item_negative_quantity(order, dish):
    # Проверка, что нельзя создать позицию с отрицательным количеством
    with pytest.raises(
        ValidationError
    ):  # Ожидаем ошибку из-за отрицательного количества
        OrderItem.objects.create(order=order, dish=dish, quantity=-1)


def test_delete_order_with_order_items(order, order_item):
    # Проверка, что удаление заказа удаляет связанные с ним позиции
    order_id = order.id
    order.delete()
    assert not OrderItem.objects.filter(order_id=order_id).exists()


@pytest.mark.django_db
def test_create_order_without_table_number():
    # Проверка создания заказа без номера стола
    with pytest.raises(
        ValidationError
    ):  # Ожидаем ошибку из-за отсутствия обязательного поля
        Order.objects.create(status="waiting")

@pytest.mark.django_db
def test_create_dish_with_invalid_price():
    # Проверка, что нельзя создать блюдо с отрицательной ценой
    with pytest.raises(ValidationError):  # Ожидаем ошибку из-за отрицательной цены
        Dish.objects.create(name="Invalid Dish", price=-5.0)
