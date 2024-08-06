from django.contrib import admin
from django.urls import path, include
from olcha import views

urlpatterns = [
    path('category/', views.CategoryListApiView.as_view(), name='category-list'),
    path('category/<int:pk>/detail/', views.CategoryDetailApiView.as_view(), name='category-detail'),
    path('category/create/', views.CategoryCreateApiView.as_view(), name='create-category'),
    path('category/<slug:slug>/edit/', views.CategoryUpdateApiView.as_view()),
    path('category/<slug:slug>/delete/', views.CategoryDeleteApiView.as_view()),

]