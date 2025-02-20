from typing import Any, Dict, Optional, Union
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.db.models import F, Sum, Q, QuerySet

from ..forms import (
    DishForm,
    OrderCreateForm,
    OrderItemFormSet,
    OrderUpdateForm,
)
from ..models import Dish, Order


class OrderListView(ListView):
    """
    Представление для отображения списка заказов.
    STATUS_TRANSLATION - Словарь для перевода строки из запроса в статус заказа
    """

    model = Order
    context_object_name = "orders"
    paginate_by = 5

    STATUS_TRANSLATION: Dict[str, Union[str, Order.Status]] = {
        "в ожидании": Order.Status.WAITING,
        "готово": Order.Status.READY,
        "оплачено": Order.Status.PAID,
    }

    def get_queryset(self) -> QuerySet[Order]:
        """
        Возвращает отсортированный по убыванию
        и отфильтрованный(если надо) список заказов.
        """
        queryset: QuerySet[Order] = Order.objects.order_by("-id")
        query: Optional[str] = self.request.GET.get("q")

        if query:
            translated_status: Optional[Union[str, Order.Status]] = (
                self.STATUS_TRANSLATION.get(query.lower())
            )
            queryset = queryset.filter(
                Q(table_number__icontains=query)
                | Q(status=translated_status if translated_status else query)
            )
        return queryset


class OrderDetailView(DetailView):
    """
    Представление для отображения о заказе.
    """

    model = Order


class OrderCreateView(CreateView):
    """
    Представление для создания нового заказа.
    """

    model = Order
    form_class = OrderCreateForm
    success_url = "/"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Добавляет в контекст набор форм для элементов заказа.
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        if self.request.POST:
            context["order_items"] = OrderItemFormSet(self.request.POST)
        else:
            context["order_items"] = OrderItemFormSet()
        return context

    def form_valid(self, form: Any) -> HttpResponse:
        """
        Обрабатывает корректно заполненную форму заказа.
        """
        context: Dict[str, Any] = self.get_context_data()
        order_items = context["order_items"]

        if form.is_valid():
            self.object: Order = form.save(commit=False)
            order_items.instance = self.object

            if order_items.is_valid():
                self.object.save()
                order_items.save()
                return redirect(self.success_url)

        context["form"] = form
        context["order_items"] = order_items
        return self.render_to_response(context)


class OrderUpdateView(UpdateView):
    """
    Представление для обновления существующего заказа.
    """

    model = Order
    form_class = OrderUpdateForm
    template_name_suffix = "_update_form"
    success_url = "/"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Добавляет в контекст набор форм для элементов заказа.
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        if self.request.POST:
            context["order_items"] = OrderItemFormSet(
                self.request.POST,
                instance=self.object,
            )
        else:
            context["order_items"] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form: Any) -> HttpResponse:
        """
        Обрабатывает корректно заполненную форму обновления заказа.
        """
        context: Dict[str, Any] = self.get_context_data()
        order_items = context["order_items"]

        if form.is_valid() and order_items.is_valid():
            self.object = form.save()
            order_items.instance = self.object
            order_items.save()
            return redirect(self.success_url)

        return self.render_to_response(context)


class OrderDeleteView(DeleteView):
    """
    Представление для удаления заказа.
    """

    model = Order
    success_url = reverse_lazy("cafe_em:order_list")


class OrderTotalSumView(TemplateView):
    """
    Представление для отображения общей суммы оплаченных заказов.
    """

    template_name = "cafe_em/total_sum.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Вычисляет общую сумму заказа, где статус заказа 'оплачено'.
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        total_sum: Optional[float] = (
            Order.objects.filter(status=Order.Status.PAID).aggregate(
                total=Sum(
                    F("order_items__quantity") * F("order_items__dish__price")
                )
            )["total"]
            or 0
        )
        context["total_sum"] = total_sum
        return context


class DishListView(ListView):
    """
    Представление для отображения списка блюд.
    """

    model = Dish
    context_object_name = "dishs"
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Dish]:
        """
        Возвращает список блюд, отсортированных по убыванию идентификатора.
        """
        return Dish.objects.order_by("-id")


class DishDetailView(DetailView):
    """
    Представление для отображения подробной информации о блюде.
    """

    model = Dish


class DishCreateView(CreateView):
    """
    Представление для создания нового блюда.
    """

    model = Dish
    form_class = DishForm
    success_url = "new_dish"
