# -*- coding: utf-8 -*-
from django.contrib.auth import login

from comment.models import Comment
from django.views.generic import TemplateView, CreateView
from django.shortcuts import reverse
from blog.models import Blog, Post
from core.models import User
from category.models import Category
from django import forms

# Create your views here.
#def base_page (request, name=''):
#        return render(request, 'core/base.html', {'name': name})

class HomePageView(TemplateView):

    template_name = "core/base.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest_articles'] = Blog.objects.order_by('-createdata')[:5]
        context['latest_categories'] = Category.objects.order_by('-created_at')[:5]
        context['blog_count'] = Blog.objects.all().count()
        context['post_count'] = Post.objects.all().count()
        context['comment_count'] = Comment.objects.all().count()
        context['category_count'] = Category.objects.all().count()
        return context


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    Username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label="")

    class Meta:
        model = User
        fields = ('Username', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["Username"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = 'core:mainpg'
    model = User
    template_name = 'core/user_form.html'

    def form_valid(self, form):
        result = super(RegistrationView, self).form_valid(form)
        login(self.request, self.object)
        return result

    def get_success_url(self):
        return reverse('core:mainpg')