from django.urls import reverse_lazy, reverse

from catalog.models import Product
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = ("name", "description", "category", "image", "price")
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = ("name", "description", "category", "image", "price")
    success_url = reverse_lazy("catalog:product_update")

    def get_success_url(self):
        return reverse ("catalog:product_detail", args=[self.kwargs.get("pk")])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")
