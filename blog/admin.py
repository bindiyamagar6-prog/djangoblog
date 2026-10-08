from django.contrib import admin
from .models import Post, Category, Tag


class StyledAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ("blog/css/style.css",)}


@admin.register(Post)
class PostAdmin(StyledAdmin):
    list_display = ("title", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)


@admin.register(Category)
class CategoryAdmin(StyledAdmin):
    list_display = ("name",)


@admin.register(Tag)
class TagAdmin(StyledAdmin):
    list_display = ("name",)