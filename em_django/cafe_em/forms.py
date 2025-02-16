from django import forms
from .models import Dish, Order, OrderItem


# class CustomOrderItemFormSet(forms.BaseInlineFormSet):
#     def clean(self):
#         """Проверяем, что нет дубликатов блюд в одном заказе"""
#         super().clean()
#         errors = []
#         dishes = []

#         for form in self.forms:
#             if form.cleaned_data and not form.cleaned_data.get(
#                 "DELETE",
#                 False,
#             ):
#                 dish = form.cleaned_data.get("dish")

#                 if dish in dishes:
#                     errors.append(f"Блюдо '{dish}' добавлено дважды.")
#                 dishes.append(dish)

#         if errors:
#             raise forms.ValidationError(errors)  # Теперь ошибка глобальная


class OrderForm(forms.ModelForm):
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
        fields = ["dish", "quantity"]

    def clean(self):
        cleaned_data = super().clean()
        dish = cleaned_data.get("dish")
        order = getattr(
            self.instance,
            "order",
            None,
        )

        if order and dish:
            existing = OrderItem.objects.filter(
                order=order,
                dish=dish,
            ).exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError(
                    "Это блюдо уже добавлено, измените количество."
                )

        return cleaned_data


OrderItemFormSet = forms.inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    # formset=CustomOrderItemFormSet,
    extra=5,
    can_delete=False,
)


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["name", "price"]
