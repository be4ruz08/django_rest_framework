from django.contrib import admin
from django.urls import path, include

from olcha.views.category import views as c_views
from olcha.views.group import views as g_views
from olcha.views.product import views as p_views
from olcha.views.auth import views as auth_views

urlpatterns = [

    # Category urls
    path('category/', c_views.CategoryListApiView.as_view(), name='category-list'),
    path('category/<int:pk>/detail/', c_views.CategoryDetailApiView.as_view(), name='category-detail'),
    path('category/create/', c_views.CategoryCreateApiView.as_view(), name='create-category'),
    path('category/<slug:slug>/edit/', c_views.CategoryUpdateApiView.as_view()),
    path('category/<slug:slug>/delete/', c_views.CategoryDeleteApiView.as_view()),

    # Group urls
    path('group/create/', g_views.GroupCreateAPIView.as_view(), name='group-create'),
    path('category/<slug:slug>/', g_views.GroupListAPIView.as_view(), name='group-list'),
    path('group/<slug:slug>/detail/', g_views.GroupDetailAPIView.as_view()),

    # Product urls
    path('product/create/', p_views.ProductCreateAPIView.as_view(), name='product-create'),
    # path('products/', p_views.ProductListAPIView.as_view(), name='product-list'),
    path('category/<slug:category_slug>/<slug:group_slug>/', p_views.ProductListAPIView.as_view(), name='product-list'),
    path('product/view/<slug:slug>/', p_views.ProductDetailAPIView.as_view()),

    # Attributes urls

    path('products/<slug:slug>/attributes/', p_views.ProductAttributeListAPIView.as_view(), name='product-attributes'),

    # Authentication

    path('login-page/', auth_views.LoginAPIView.as_view()),
    path('logout-page/', auth_views.LogoutAPIView.as_view()),
    path('register-page/', auth_views.RegisterAPIView.as_view()),

]