import os
import django
import pytest

from cafe_em.models import Dish, Order, OrderItem

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "em_django.settings")
django.setup()

pytestmark = pytest.mark.django_db


@pytest.fixture
def dish(db):
    return Dish.objects.create(name="Борщ", price=3.5)


@pytest.fixture
def order(db):
    return Order.objects.create(table_number=1, status="waiting")


@pytest.fixture
def order_item(db, order, dish):
    return OrderItem.objects.create(order=order, dish=dish, quantity=2)


def test_unique_table_number(db):
    Order.objects.create(table_number=1, status="waiting")
    with pytest.raises(Exception):
        Order.objects.create(table_number=1, status="waiting")
