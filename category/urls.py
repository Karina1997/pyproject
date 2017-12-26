from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from category.views import *

urlpatterns = [
    url(r'^$', CategoryList.as_view(), name='categoriespage'),
    url(r'^(?P<ident>\d+)$', OneCategory.as_view() , name='onecategory'),
    url(r'^new$', login_required(NewCategory.as_view()), name='newcategory'),
]
