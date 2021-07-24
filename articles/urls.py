from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('my_posts/', views.MyPosts.as_view(), name='my_posts'),
    path('create_blog/', views.create_blog_view, name='create_blog'),
    path('search/', views.search, name='search'),
    path('submit/<slug:slug>/', views.comment, name='submit'),
    path('<slug:slug>/', views.articledetailview, name='detail'),
    path('<slug:slug>/edit/', views.update_blog_view, name='edit'),


]

