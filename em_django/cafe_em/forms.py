from django import forms
from .models import Dish, Order, OrderItem


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table_number"]

    def clean_table_number(self):
        table_number = self.cleaned_data["table_number"]
        if Order.objects.filter(table_number=table_number).exists():
            raise forms.ValidationError("Номер стола уже занят.")
        return table_number


class OrderItemForm(forms.ModelForm):
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
    extra=5,
    can_delete=False,
)


class OrderUpdateForm(forms.ModelForm):
    class Meta(OrderCreateForm.Meta):
        fields = [
            "table_number",
            "status",
        ]


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "price"]
