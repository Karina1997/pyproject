# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView
from .models import Category
from blog.models import Blog


class CategoryList(ListView):
    template_name = "category/allcategories.html"
    context_object_name = 'categories'
    model = Category


class OneCategory(ListView):
    template_name = "category/onecategory.html"
    context_object_name = 'blogs'
    model = Blog

    def get_context_data(self, **kwargs):
        context = super(OneCategory, self).get_context_data(**kwargs)
        context['category_name'] = self.category.name
        return context

    def get_queryset(self):
        return Blog.objects.filter(category=self.category)

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, id=self.kwargs['ident'])
        return super(OneCategory, self).dispatch(request, *args, **kwargs)


class NewCategory(CreateView):
    template_name = 'category/newcategory.html'
    model = Category
    context_object_name = 'newcategory'
    fields = ('name',)

    def get_success_url(self):
        return reverse('category:onecategory', kwargs={'ident': self.object.id})
