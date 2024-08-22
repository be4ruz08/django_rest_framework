from django.urls import path
from post import views
#
# from post.views import PostViewSet
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register('post', PostViewSet, basename='post')
#
# urlpatterns = [
#     path('post-list/', views.PostAPIView.as_view()),
#     path('post-actions/', views.PostModelViewSet.as_view()),
#     path('post-actions/<int:pk>/', views.PostDetailAPIView.as_view())
# ] + router.urls

urlpatterns = [
    path('post-list/', views.PostListAPIView.as_view()),
    path('post-list/<int:pk>', views.PostDetailAPIView.as_view())
]