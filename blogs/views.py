from django.urls import reverse_lazy, reverse

from blogs.forms import PostForm
from blogs.models import Post
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(publication_sign=True)


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("blogs:post_list")


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("blogs:post_update")

    def get_success_url(self):
        return reverse("blogs:post_detail", args=[self.kwargs.get("pk")])


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("blogs:post_list")
