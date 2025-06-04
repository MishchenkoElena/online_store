from django.urls import path
from blogs.apps import BlogsConfig
from blogs.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
app_name = BlogsConfig.name
urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("blogs/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("blogs/create/", PostCreateView.as_view(), name = "post_create"),
    path("blogs/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("blogs/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
]
