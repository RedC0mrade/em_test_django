from django import forms
from .models import Dish, Order, OrderItem


class OrderCreateForm(forms.ModelForm):
    """
    Форма для создания заказа, включает только номер стола.
    """

    class Meta:
        model = Order
        fields = ["table_number"]

    def clean_table_number(self) -> int:
        """
        Проверяет, не занят ли указанный номер стола.
        """
        table_number = self.cleaned_data["table_number"]
        if Order.objects.filter(table_number=table_number).exists():
            raise forms.ValidationError("Номер стола уже занят.")
        return table_number


class OrderItemForm(forms.ModelForm):
    """
    Форма для создания и редактирования позиций заказа.
    """

    class Meta:
        model = OrderItem
        fields = [
            "dish",
            "quantity",
        ]


OrderItemFormSet = forms.inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=4,
    can_delete=False,
)


class OrderUpdateForm(forms.ModelForm):
    """
    Форма для обновления заказа.
    """

    class Meta(OrderCreateForm.Meta):
        fields = [
            "table_number",
            "status",
        ]


class DishForm(forms.ModelForm):
    """
    Форма для создания и редактирования блюд.
    """

    class Meta:
        model = Dish
        fields = [
            "name",
            "price",
        ]

