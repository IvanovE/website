from django.contrib import admin
from .models import Author, Tag, Post, Comment, UserSeenPosts

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_filter = ["author", "date", "tags", ]
    list_display = ["title", "date", "author", ]
    prepopulated_fields = {"slug": ("title", )}


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", ]


class CommentForm(admin.ModelAdmin):
    list_display = ["user", "post", "date", ]
    list_filter = ["user", ]


class UserSeenPostsAdmin(admin.ModelAdmin):
    list_display = ["user", "post", ]
    list_filter = ["user", "post", ]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentForm)
admin.site.register(UserSeenPosts, UserSeenPostsAdmin)
