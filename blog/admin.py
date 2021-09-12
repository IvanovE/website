from django.contrib import admin
from .models import Author, Tag, Post, Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_filter = ["author", "date", "tags", ]
    list_display = ["title", "date", "author", ]
    prepopulated_fields = {"slug": ("title", )}


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", ]


class CommentForm(admin.ModelAdmin):
    list_display = ["user_name", "post", "user_email", "date", ]
    list_filter = ["user_name", "user_email", ]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentForm)
