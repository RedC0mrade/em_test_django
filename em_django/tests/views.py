import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from cafe_em.models import Dish, Order, OrderItem


@pytest.mark.django_db
class TestOrderAPI:
    """
    Тесты для представлений, связанных с заказами.
    """

    def setup_method(self):
        self.client = APIClient()
        self.dish = Dish.objects.create(
            name="Борщ",
            price=10.00,
        )
        self.order = Order.objects.create(
            table_number=1,
            status="waiting",
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            dish=self.dish,
            quantity=2,
        )

    def test_create_order(self):
        """
        Тест на корректные данные запроса
        заказов и после создания создание заказа
        """
        url = reverse("cafe_em:order-list")
        data = {
            "table_number": 2,
            "status": "waiting",
        }
        response = self.client.get(url)
        assert len(response.data) == 1
        response = self.client.post(
            url,
            data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["table_number"] == 2
        assert response.data["status"] == "waiting"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_filter_by_status(self):
        """
        Тест на корректное отображение сортировки по статусу готовности
        """
        url = reverse(
            "cafe_em:order-filter-by-status",
            kwargs={"status": "waiting"},
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        Order.objects.create(
            table_number=2,
            status="waiting",
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        Order.objects.create(
            table_number=3,
            status="paid",
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_partial_update_order(self):
        """
        Тест на корректность внесения изменения статуса заказа
        """
        url = reverse(
            "cafe_em:order-partial-update-order",
            kwargs={"pk": self.order.id},
        )
        data = {"status": "ready"}
        response = self.client.patch(
            url,
            data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "ready"
        data = {"status": "wrong_status"}
        response = self.client.patch(
            url,
            data,
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_order(self):
        """Тест на корректное удаление стола"""
        url = reverse(
            "cafe_em:order-delete-order",
            kwargs={"pk": self.order.id},
        )
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Order.objects.filter(id=self.order.id).exists()
        url = reverse(
            "cafe_em:order-delete-order",
            kwargs={"pk": self.order.id},
        )
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_total_sum(self):
        """Тест на корректное отображение блока общая сумма"""
        self.order.status = "paid"
        self.order.save()
        url = reverse("cafe_em:order-total-sum")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_sum"] == 20.00
        order = Order.objects.create(
            table_number=2,
            status="paid",
        )
        OrderItem.objects.create(
            order=order,
            dish=self.dish,
            quantity=3,
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_sum"] == 50.00
        order = Order.objects.create(
            table_number=3,
            status="ready",
        )
        OrderItem.objects.create(
            order=order,
            dish=self.dish,
            quantity=3,
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_sum"] == 50.00


@pytest.mark.django_db
class TestDishAPI:
    def setup_method(self):
        self.client = APIClient()
        self.dish = Dish.objects.create(
            name="Борщ",
            price=10.00,
        )

    def test_create_dish(self):
        """Проверяем корректность создания блюда"""
        url = reverse("cafe_em:dish-list")
        data = {"name": "Вареники", "price": 100.00}
        response = self.client.post(
            url,
            data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Вареники"

    def test_create_dish_with_incorrect_data(self):
        """Проверяем корректность создания блюда"""
        url = reverse("cafe_em:dish-list")
        data = {"name": "Вареники", "price": "ten $"}
        response = self.client.post(
            url,
            data,
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_dishes(self):
        """Проверяем корректность отображения блюд"""
        url = reverse("cafe_em:dish-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        data = {"name": "Вареники", "price": 100.00}
        response = self.client.post(
            url,
            data,
            format="json",
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_retrieve_dish(self):
        """Проверяем корректность отображения блюдa"""
        url = reverse(
            "cafe_em:dish-detail",
            kwargs={"pk": self.dish.id},
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Борщ"

    def test_retrieve_dish_with_incorrect_pk(self):
        """Проверяем корректность обработки не правильного id блюда"""
        wrong_pk = 2
        url = reverse(
            "cafe_em:dish-detail",
            kwargs={"pk": wrong_pk},
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_dish(self):
        url = reverse(
            "cafe_em:dish-detail",
            kwargs={"pk": self.dish.id},
        )
        data = {"name": "Жаркое", "price": 20.00}
        response = self.client.put(
            url,
            data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Жаркое"

    def test_update_dishwith_incorrect_pk(self):
        wrong_pk = 2
        url = reverse(
            "cafe_em:dish-detail",
            kwargs={"pk": wrong_pk},
        )
        data = {"name": "Жаркое", "price": 20.00}
        response = self.client.put(
            url,
            data,
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_dish(self):
        """Проверяем корректность удаления блюда"""
        url = reverse(
            "cafe_em:dish-detail",
            kwargs={"pk": self.dish.id},
        )
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Dish.objects.filter(id=self.dish.id).exists()

    def test_delete_dish_with_incorrect_pk(self):
        """Проверяем корректность удаления блюда"""
        wrong_pk = 2
        url = reverse(
            "cafe_em:dish-detail",
            kwargs={"pk": wrong_pk},
        )
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
