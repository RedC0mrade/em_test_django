from typing import Any

from django.contrib import admin


from .models import Dish, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Встроенная модель для отображения позиций заказа.
    """

    model = OrderItem
    extra = 1


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """
    Администрирование модели Dish.
    Отображает их ID, названием и ценой.
    """

    list_display: tuple[str, str, str] = (
        "id",
        "name",
        "price",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Администрирование модели Order.
    Отображает список заказов с номером стола, статусом и общей суммой заказа.
    """

    list_display: tuple[str, str, str, str] = (
        "id",
        "table_number",
        "status",
        "total_price",
    )
    list_filter: tuple[str, ...] = (
        "id",
        "table_number",
        "status",
    )
    search_fields: tuple[str, ...] = ("table_number",)
    readonly_fields: tuple[str, ...] = ("total_price",)
    inlines = [OrderItemInline]

    def total_price(self, obj: Order) -> Any:
        """
        Метод для отображения общей суммы заказа.
        """
        return obj.total_price()

    total_price.short_description = "Сумма заказа"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Администрирование модели OrderItem.
    Отображает id заказa, id блюда и их количество в заказе.
    """

    list_display: tuple[str, str, str] = (
        "order",
        "dish",
        "quantity",
    )
