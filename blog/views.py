from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View

from .models import Post
from .forms import CommentForm


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-time']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class PostsView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    ordering = ['-time']
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

        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': CommentForm(),
            'all_comments': post.comments.all().order_by('-time'),
            'saved_for_later': self.is_stored_post(request, post.id)
        }

        return render(request, 'blog/post-detail.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page', args=[slug]))

        context = {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': comment_form,
            'all_comments': post.comments.all().order_by('-time'),
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

        return HttpResponseRedirect('/')
