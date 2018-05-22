# coding: utf-8
from django.conf.urls import url
from blog.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', BlogList.as_view(), name='listOfBlogs'),
    url(r'^(?P<ident>\d+)/$', PostList.as_view(), name='blogWithItsPosts'),
    url(r'^post/(?P<pk>\d+)/edit/', login_required(PostUpdate.as_view()), name='edit_post'),
    url(r'^post/(?P<ident>\d+)/$', PostPage.as_view(), name='concretePost'),
    url(r'^post/(?P<ident>\d+)/like/$', PostLikeAjaxView.as_view(), name='post_ajax_like'),
    url(r'^new/', login_required(NewBlog.as_view()), name='new_blog'),
    url(r'^(?P<pk>\d+)/edit/', login_required(BlogUpdate.as_view()), name='edit_blog'),
    url(r'^(?P<ident>\d+)/new/$', login_required(NewPost.as_view()), name='new_post'),
]