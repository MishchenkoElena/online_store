from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Category
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from catalog.services import get_products_category


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("catalog.can_unpublish_product") or user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


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


class ProductsCategoryListView(ListView):
    model = Product
    template_name = "catalog/product_category_list.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        self.category = get_object_or_404(Category, id=category_id)
        return get_products_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context

    def base_view(request):
        categories = Category.objects.all()
        return render(request, "base.html", {"categories": categories})


class CategoryListView(ListView):
    model = Category
    template_name = "catalog/base.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
