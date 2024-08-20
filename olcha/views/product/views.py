from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from olcha.models import Product, Attribute
from olcha.serializers import ProductModelSerializer, AttributeSerializer
from rest_framework import viewsets
from olcha.permissions import CustomPermission


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductModelSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        group_slug = self.kwargs.get('group_slug')
        queryset = Product.objects.filter(
            group__category__slug=category_slug,
            group__slug=group_slug
        ).select_related('group__category')
        return queryset


class ProductAttributeListAPIView(ListAPIView):
    serializer_class = AttributeSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Attribute.objects.filter(
            product__slug=slug
        ).select_related('key', 'value')


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.select_related('group')
    serializer_class = ProductModelSerializer
    permission_classes = [CustomPermission]
    lookup_field = 'slug'



