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
from django.db.models import F, Sum, Q

from .forms import DishForm, OrderCreateForm, OrderItemFormSet, OrderUpdateForm
from .models import Dish, Order


class OrderListView(ListView):
    model = Order
    context_object_name = "orders"
    paginate_by = 5

    STATUS_TRANSLATION = {
        "в ожидании": Order.Status.WAITING,
        "готово": Order.Status.READY,
        "оплачено": Order.Status.PAID,
    }

    def get_queryset(self):
        queryset = Order.objects.order_by("-id")
        query = self.request.GET.get("q")

        if query:
            translated_status = self.STATUS_TRANSLATION.get(query.lower())

            queryset = queryset.filter(
                Q(table_number__icontains=query)
                | Q(status=translated_status if translated_status else query)
            )

        return queryset


class DishListView(ListView):
    model = Dish
    context_object_name = "dishs"
    paginate_by = 5

    def get_queryset(self):
        return Dish.objects.order_by("-id")


class OrderDetailView(DetailView):
    model = Order


class DishDetailView(DetailView):
    model = Dish


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["order_items"] = OrderItemFormSet(self.request.POST)
        else:
            context["order_items"] = OrderItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context["order_items"]

        if form.is_valid():
            self.object = form.save(
                commit=False
            )
            order_items.instance = self.object

            if order_items.is_valid():
                self.object.save()
                order_items.save()
                return redirect(self.success_url)

        context["form"] = form
        context["order_items"] = order_items
        return self.render_to_response(context)


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name_suffix = "_update_form"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["order_items"] = OrderItemFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["order_items"] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context["order_items"]

        if form.is_valid() and order_items.is_valid():
            self.object = form.save()
            order_items.instance = self.object
            order_items.save()
            return redirect(self.success_url)

        return self.render_to_response(context)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("cafe_em:order_list")


class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    success_url = "new_dish"


class OrderTotalSumView(TemplateView):
    template_name = "cafe_em/total_sum.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_sum = (
            Order.objects.filter(status=Order.Status.PAID).aggregate(
                total=Sum(
                    F("order_items__quantity") * F("order_items__dish__price")
                )
            )["total"]
            or 0
        )

        context["total_sum"] = total_sum
        return context
