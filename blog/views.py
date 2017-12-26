# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, View
from django.shortcuts import render, get_object_or_404, reverse
from .models import Blog, Post, Like
from comment.models import Comment
from category.models import Category
from django import forms
from django.db import models
from django.http import HttpResponse


# Create your views here.
# def blog_page (request, name=''): #список блогов
#   return render(request, 'blog/blogpage.html', {'blogs': Blog.objects.all()})

class PostPage(CreateView):
    template_name = "blog/post_page.html"
    context_object_name = 'post'
    model = Comment
    fields = ('text',)

    def dispatch(self, request, *args, **kwargs):
        self.postobject = get_object_or_404(Post, id=self.kwargs['ident'])
        #  self.blogobject = get_object_or_404(Blog, id=self.kwargs['identer'])
        return super(PostPage, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostPage, self).get_context_data(**kwargs)
        context['post'] = self.postobject
        context['blog'] = self.postobject.blog
        context['comment_list'] = Comment.objects.filter(post=self.postobject)
        context['likes'] = Like.objects.filter(post=self.postobject).count()
        return context

    def get_success_url(self):
        return reverse('blog:concretePost', kwargs={'ident': self.object.post.id})

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.post_id = self.kwargs['ident']
            form.instance.author = self.request.user
            return super(PostPage, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse('core:login'))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = 'postname', 'text'


class PostList(ListView):
    template_name = "blog/posts_list.html"
    context_object_name = 'posts'
    model = Post
    paginate_by = 10

    def get_queryset(self):
        self.blog = get_object_or_404(Blog, id=self.kwargs['ident'])
        return Post.objects.filter(blog=self.blog)

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['blog_id'] = self.kwargs['ident']
        context['blog'] = self.blog
        context['categorylist'] = Category.objects.filter(blog=self.blog)

        for post in context['posts']:
            post.form = PostForm(instance=post)

        return context


class BlogList(ListView):
    template_name = "blog/blogpage.html"
    context_object_name = 'blogs'
    model = Blog

    def get_queryset(self):

        q = super(BlogList, self).get_queryset()

        self.form = BlogsListForm(self.request.GET)

        if self.form.is_valid():
            if self.form.cleaned_data['postscount']:
                q = q.annotate(post_count=models.Count('posts__id')).filter(
                    post_count=self.form.cleaned_data['postscount'])
            if self.form.cleaned_data['order_by']:
                q = q.order_by(self.form.cleaned_data['order_by'])
            if self.form.cleaned_data['search']:
                q = q.filter(name=self.form.cleaned_data['search'])
        return q

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['searchform'] = self.form
        return context


class NewPost(CreateView):
    template_name = 'blog/newpost.html'
    model = Post
    context_object_name = 'newpost'
    fields = 'postname', 'text'

    def dispatch(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog, id=self.kwargs['ident'])
        return super(NewPost, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:concretePost', kwargs={'ident': self.object.id})

    def form_valid(self, form):
        if self.blog.author == self.request.user:
            form.instance.blog_id = self.kwargs['ident']
            form.instance.author = self.request.user
            return super(NewPost, self).form_valid(form)
        else:
            # return HttpResponseRedirect(reverse('blog:change'))
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(NewPost, self).get_context_data(**kwargs)
        context['blog_id'] = self.kwargs['ident']
        return context


class NewBlog(CreateView):
    template_name = 'blog/newblog.html'
    model = Blog
    context_object_name = 'newblog'
    fields = ('name', 'category',)

    def get_success_url(self):
        return reverse('blog:blogWithItsPosts', kwargs={'ident': self.object.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NewBlog, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NewBlog, self).get_context_data(**kwargs)

        return context


class PostLikeAjaxView(View):
    def dispatch(self, request, *args, **kwargs):
        # Забираем из базы пост, который собираются лайкнуть
        self.post_object = get_object_or_404(Post, id=self.kwargs['ident'])
        return super(PostLikeAjaxView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated() or not self.post_object.likes.filter(
                author=self.request.user).exists():
            b2 = Like(author=self.request.user, post=self.post_object)
            b2.save()
            return HttpResponse(Like.objects.filter(post=self.post_object).count())


class PostUpdate(UpdateView):
    template_name = 'blog/edit_blog.html'
    model = Post
    fields = 'postname', 'text'

    def form_valid(self, form):
        if self.object.author == self.request.user:
            return super(PostUpdate, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse('blog:change'))

    def get_queryset(self):
        return super(PostUpdate, self).get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse('blog:concretePost', kwargs={'ident': self.object.id})


class BlogsListForm(forms.Form):
    order_by = forms.ChoiceField(choices=(
        ('name', 'name asc'),
        ('-name', 'name desc'),
        ('createdata', 'create data asc'),
        ('-createdata', 'create data dsc'),

    ), required=False)
    search = forms.CharField(required=False)
    postscount = forms.IntegerField(required=False)
