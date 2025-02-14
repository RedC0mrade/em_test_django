from django.contrib import admin

from cafe_em.models import Dish, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "table_number",
        "status",
        "total_price",
    )
    list_filter = (
        "id",
        "table_number",
        "status",
    )
    search_fields = ("table_number",)
    readonly_fields = ("total_price",)

    def total_price(self, obj):
        return obj.total_price()

    total_price.short_description = "Сумма заказа"

    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "dish",
        "quantity",
    )
