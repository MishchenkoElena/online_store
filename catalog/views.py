from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("catalog.can_unpublish_product") or user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(is_published=True)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.owner = self.request.user
        else:
            form.add_error(None, "Пользователь не авторизован")
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_update")

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        """Если у пользователя есть право изменять статус публикации продукта, то выводится форма
        ProductModeratorForm"""
        user = self.request.user
        product = self.get_object()
        if user == product.owner:
            return ProductForm
        elif user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied("У вас нет прав на редактирование этого продукта")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        product = self.get_object()
        if user == product.owner:
            return super().dispatch(request, *args, **kwargs)

        if (
            user.has_perm("catalog.can_delete_product")
            and user.has_perm("catalog.can_unpublish_product")
            or user.groups.filter(name="Moderator_products").exists()
        ):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()
