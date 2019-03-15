from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^homepage/$',views.search, name='search_page'),
    url(r'^article/(?P<article_id>[0-9]+)$', views.article_page, name='article_page'),
    url(r'^search_result/$', views.search_result, name='search_result'),

]