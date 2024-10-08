from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from post.models import Post
from post.serializers import PostSerializer
from post import permissions as custom_permissions
from django.core.cache import cache

# Create your views here.

# class PostAPIView(ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class PostModelViewSet(APIView):
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             data = {
#                 'success': True,
#                 'data': serializer.data
#             }
#             return Response(data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         try:
#             post = Post.objects.get(id=pk)
#         except Post.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class PostDetailAPIView(APIView):
#     def get(self, request, pk, format=None):
#         post = Post.objects.get(id=pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         try:
#             post = Post.objects.get(id=pk)
#         except Post.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         pass
#
#     def delete(self, request, pk):
#         pass
#
#
# class PostViewSet(ModelViewSet):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()


class PostAPIView(APIView, PageNumberPagination):
    permission_classes = [permissions.AllowAny]
    page_size = 100

    def get(self, request, *args, **kwargs):
        cache_key = 'post_list'
        posts = cache.get(cache_key)
        if posts is None:
            posts = Post.objects.all()
            results = self.paginate_queryset(posts, request, view=self)

            serializer = PostSerializer(results, many=True)
            cache.set(cache_key, serializer.data, timeout=60 * 5)
            return self.get_paginated_response(serializer.data)
        return Response(posts)


class PostDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        cache_key = f'post_detail_{post_id}'
        post = cache.get(cache_key)

        if post is None:
            try:
                post_obj = Post.objects.get(id=post_id)
                post = PostSerializer(post_obj).data
                cache.set(cache_key, post, timeout=60 * 3)
            except Post.DoesNotExist:
                return Response({'detail': 'Not found.'}, status=404)

        return Response(post)
    