from django.contrib import admin
from blogs.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "publication_sign",)
    list_filter = ("title",)
    search_fields = (
        "title",
        "content",
    )
