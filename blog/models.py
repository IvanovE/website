from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name()


class Tag(models.Model):
    caption = models.CharField(max_length=10)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.caption


class Post(models.Model):
    title = models.CharField(max_length=20)
    views = models.IntegerField(default=0)
    excerpt = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posts', null=True)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True, null=True)
    slug = models.SlugField(unique=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.title}, {self.author}, {self.date}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False)
    user_text = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateField(auto_now=True, null=True)
    time = models.TimeField(auto_now=True, null=True)

    def __str__(self):
        return 'Comment {} by {}'.format(self.user_text, self.user)


class UserSeenPosts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seen_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}, {self.post}'
