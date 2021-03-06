from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Post, UserSeenPosts, Tag
from .forms import CommentForm, CreateUserForm


class StartingPageView(View):
    def get(self, request):
        popular_posts = Post.objects.order_by('-views')[:3]
        new_posts = Post.objects.order_by('-date_time')[:3]
        context = {
            'popular_posts': popular_posts,
            'new_posts': new_posts
        }

        return render(request, 'blog/index.html', context)


class PostsView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    ordering = ['-date_time']
    context_object_name = 'posts'


class PostDetailView(View):
    def is_stored_post(self, request, post_id):
        read_later_post_list = request.session.get('read_later_post_list')
        if read_later_post_list is not None:
            is_saved_for_later = post_id in read_later_post_list
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(tags__in=post.tags.all()).exclude(slug=slug)[:3]

        try:
            if UserSeenPosts.objects.filter(post=post, user=request.user).exists():
                pass
            else:
                post.views += 1
                post.save()
                UserSeenPosts.objects.create(user=request.user, post=post)
        except:
            pass

        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'related_posts': related_posts,
            'comment_form': CommentForm(),
            'all_comments': post.comments.all().order_by('-date_time'),
            'saved_for_later': self.is_stored_post(request, post.id)
        }

        return render(request, 'blog/post-detail.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(tags__in=post.tags.all())[:3]

        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page', args=[slug]))

        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'related_posts': related_posts,
            'comment_form': comment_form,
            'user_name': request.user.username,
            'all_comments': post.comments.all().order_by('-date_time'),
            'saved_for_later': self.is_stored_post(request, post.id)
        }

        return render(request, 'blog/post-detail.html', context)


class ReadLaterView(View):
    def get(self, request):
        read_later_post_list = request.session.get('read_later_post_list')
        context = {}

        if read_later_post_list is None or len(read_later_post_list) == 0:
            context['posts'] = []
            context['has_posts'] = False

        else:
            posts = Post.objects.filter(id__in=read_later_post_list)
            context['posts'] = posts
            context['has_posts'] = True

        return render(request, 'blog/read-later-page.html', context)

    def post(self, request):
        read_later_post_list = request.session.get('read_later_post_list')

        if read_later_post_list is None:
            read_later_post_list = []

        post_id = int(request.POST['post_id'])
        if post_id not in read_later_post_list:
            read_later_post_list.append(post_id)
        else:
            read_later_post_list.remove(post_id)
        request.session['read_later_post_list'] = read_later_post_list

        return redirect('read-later-page')


class CategoriesView(ListView):
    template_name = 'blog/categories.html'
    model = Tag
    context_object_name = 'tags'


class CategoryView(View):
    def get(self, request, slug):
        posts = Post.objects.filter(tags__slug=slug)
        tag = Tag.objects.get(slug=slug)

        context = {
            'posts': posts,
            'tag': tag
        }

        return render(request, 'blog/category.html', context)


class SearchResultsView(View):
    template_name = 'blog/search_results.html'
    context = {}

    def get(self, request):
        query = request.GET.get('q')
        if query is not None:
            posts = Post.objects.filter(title__icontains=query)
            context = {
                'posts': posts
            }

        return render(request, 'blog/search_results.html', context)


class SignIn(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('starting-page')
        context = {}
        return render(request, 'blog/login.html', context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password2')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('starting-page')
        else:
            messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'blog/login.html', context)


class SignUp(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('starting-page')
        context = {'form': CreateUserForm()}
        return render(request, 'blog/register.html', context)

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        form = CreateUserForm({
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2})
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')

        context = {'form': form}
        return render(request, 'blog/register.html', context)


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('starting-page')
