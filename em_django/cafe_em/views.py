from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import DishForm, OrderCreateForm, OrderItemFormSet, OrderUpdateForm
from .models import Dish, Order


class OrderListView(ListView):
    model = Order
    context_object_name = "orders"
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.order_by("-id")


class DishListView(ListView):
    model = Dish
    context_object_name = "dishs"
    paginate_by = 5

    def get_queryset(self):
        return Dish.objects.order_by("-id")


class OrderDetailView(DetailView):
    model = Order

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            return render(request, "cafe_em/404_not_found.html", status=404)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class DishDetailView(DetailView):
    model = Dish

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            return render(request, "cafe_em/404_not_found.html", status=404)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


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
            self.object = form.save(commit=False)  # Заказ создаём, но НЕ сохраняем
            order_items.instance = self.object  # Передаём заказ в формсет

            if order_items.is_valid():
                self.object.save()  # Теперь сохраняем заказ
                order_items.save()  # Теперь сохраняем OrderItem'ы
                return redirect(self.success_url)

        context["form"] = form
        context["order_items"] = order_items  # Передаём существующий formset
        return self.render_to_response(context)

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name_suffix = "_update_form"
    success_url = "/"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["order_items"] = OrderItemFormSet(self.request.POST, instance=self.object)
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

class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    success_url = "/"
