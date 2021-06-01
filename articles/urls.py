from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('add/', views.AddPostView.as_view(), name='add'),
    path('search/', views.search, name='search'),
    path('submit/<slug:slug>/', views.post_detail, name='submit'),
    path('<slug:slug>/', views.articledetailview, name='detail'),

]

