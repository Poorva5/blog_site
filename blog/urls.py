from django.contrib.contenttypes.fields import create_generic_related_manager
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from .feeds import LatestPostsFeed
from blog.views import *

app_name = 'blog'

urlpatterns = [ 
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag' ),
    #  path('', views.PostListView.as_view(), name= 'post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('create/', create_post, name='create_post'),
]