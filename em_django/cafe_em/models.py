from typing import Any

from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError


class Dish(models.Model):
    """
    Модель блюда.
    """

    class Meta:
        verbose_name = "Dish"

    name: str = models.CharField(
        max_length=255,
        verbose_name="Название блюда",
    )
    price: float = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )

    def clean(self):
        if self.price < 0:
            raise ValidationError("Цена не может быть отрицательной")
    
    def save(self, *args, **kwargs):
        """
        Проверка корректности данных перед сохранением.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    """
    Модель заказа
    """

    class Status(models.TextChoices):
        WAITING = "waiting", "В ожидании"
        READY = "ready", "Готово"
        PAID = "paid", "Оплачено"

    class Meta:
        verbose_name = "Order"

    table_number: int = models.PositiveIntegerField(
        verbose_name="Номер стола",
        unique=True,
        null=False,
    )
    status: str = models.CharField(
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

    def total_price(self) -> float:
        """
        Общая стоимость заказа.
        """
        return sum(
            item.dish.price * item.quantity
            for item in self.order_items.prefetch_related("dish").all()
        )

    def clean(self):
        """
        Проверка статуса
        """
        if self.status not in self.Status:
            raise ValidationError(f"Неверный статус: {self.status}")

    def save(self, *args, **kwargs):
        """
        Проверка корректности данных перед сохранением.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Заказ {self.id} - Стол {self.table_number}"


class OrderItem(models.Model):
    """
    Модель связывающая заказ и блюдо.
    """

    order: Order = models.ForeignKey(
        Order,
        related_name="order_items",
        on_delete=models.CASCADE,
        verbose_name="Заказ",
    )
    dish: Dish = models.ForeignKey(
        Dish,
        related_name="ordered_in",
        on_delete=models.CASCADE,
        verbose_name="Блюдо",
    )
    quantity: int = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество",
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = "Order Item"
        constraints = [
            models.UniqueConstraint(
                fields=["order", "dish"],
                name="unique_order_dish",
            )
        ]

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Проверка корректности данных перед сохранением.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.dish.name} - {self.quantity}шт"
