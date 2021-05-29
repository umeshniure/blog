from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('<slug:slug>/', views.post_detail, name='detail'),
    path('add/', views.AddPostView.as_view(), name='add'),
    path('search/', views.search, name='search'),
]
