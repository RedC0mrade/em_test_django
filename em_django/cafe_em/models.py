from django.db import models
from django.forms import ValidationError


class Dish(models.Model):

    class Meta:
        verbose_name = "Dish"

    name = models.CharField(
        max_length=255,
        verbose_name="Название блюда",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        WAITING = "waiting", "В ожидании"
        READY = "ready", "Готово"
        PAID = "paid", "Оплачено"

    class Meta:
        verbose_name = "Order"

    table_number = models.PositiveIntegerField(verbose_name="Номер стола")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.WAITING,
        verbose_name="Статус заказа",
    )
    items = models.ManyToManyField(
        Dish,
        through="OrderItem",
        verbose_name="Заказанные блюда",
    )

    def total_price(self):
        return sum(
            item.dish.price * item.quantity
            for item in self.order_items.prefetch_related("dish").all()
        )

    def __str__(self):
        return f"Заказ {self.id} - Стол {self.table_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="order_items",
        on_delete=models.CASCADE,
    )
    dish = models.ForeignKey(
        Dish,
        related_name="ordered_in",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество",
    )

    class Meta:
        verbose_name = "Order Item"
        constraints = [
            models.UniqueConstraint(
                fields=["order", "dish"],
                name="unique_order_dish",
            )
        ]

    def clean(self):
        """Проверяем на случайное дублирование позиции в заказе"""
        if not self.order_id or not self.dish_id:
            return
        if (
            OrderItem.objects.filter(
                order=self.order,
                dish=self.dish,
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                "Это блюдо уже добавлено в заказ, измените количество."
            )
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"
