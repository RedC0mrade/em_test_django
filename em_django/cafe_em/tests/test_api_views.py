import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from cafe_em.models import Dish, Order, OrderItem


@pytest.mark.django_db
class TestOrderAPI:
    def setup_method(self):
        self.client = APIClient()
        self.dish = Dish.objects.create(name="Борщ", price=10.00)
        self.order = Order.objects.create(table_number=1, status="waiting")
        self.order_item = OrderItem.objects.create(
            order=self.order, dish=self.dish, quantity=2
        )

    def test_create_order(self):
        url = reverse("cafe_em:order-list")
        data = {
            "table_number": 2,
            "status": "waiting",
        }

        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["table_number"] == 2
        assert response.data["status"] == "waiting"

    def test_list_orders(self):
        url = reverse("cafe_em:order-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        Order.objects.create(table_number=2, status="waiting")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_filter_by_status(self):
        url = reverse(
            "cafe_em:order-filter-by-status",
            kwargs={"status": "waiting"},
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        Order.objects.create(table_number=2, status="waiting")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        Order.objects.create(table_number=3, status="paid")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2



    def test_partial_update_order(self):
        url = reverse("cafe_em:order-partial-update-order", kwargs={"pk": self.order.id})
        data = {"status": "ready"}
        response = self.client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "ready"

#     def test_delete_order(self):
#         url = reverse("order-delete-order", kwargs={"pk": self.order.id})
#         response = self.client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not Order.objects.filter(id=self.order.id).exists()

#     def test_total_sum(self):
#         self.order.status = "paid"
#         self.order.save()
#         url = reverse("order-total-sum")
#         response = self.client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["total_sum"] == 20.00  # 2 * 10.00


# @pytest.mark.django_db
# class TestDishAPI:
#     def setup_method(self):
#         self.client = APIClient()
#         self.dish = Dish.objects.create(name="Пельмени", price=15.00)

#     def test_create_dish(self):
#         url = reverse("dish-list")
#         data = {"name": "Вареники", "price": 12.50}
#         response = self.client.post(url, data, format="json")
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data["name"] == "Вареники"

#     def test_list_dishes(self):
#         url = reverse("dish-list")
#         response = self.client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1  # Уже есть 1 блюдо

#     def test_retrieve_dish(self):
#         url = reverse("dish-detail", kwargs={"pk": self.dish.id})
#         response = self.client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == "Пельмени"

#     def test_update_dish(self):
#         url = reverse("dish-detail", kwargs={"pk": self.dish.id})
#         data = {"name": "Жаркое", "price": 20.00}
#         response = self.client.put(url, data, format="json")
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["name"] == "Жаркое"

#     def test_delete_dish(self):
#         url = reverse("dish-detail", kwargs={"pk": self.dish.id})
#         response = self.client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not Dish.objects.filter(id=self.dish.id).exists()
