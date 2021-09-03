from django.contrib import admin
from .models import Author, Tag, Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_filter = ["author", "date", "tags", ]
    list_display = ["title", "date", "author", ]
    prepopulated_fields = {"slug": ("title", )}


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", ]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
