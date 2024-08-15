from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from olcha.models import Product, Attribute
from olcha.serializers import ProductModelSerializer, AttributeSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        group_slug = self.kwargs.get('group_slug')
        queryset = Product.objects.filter(group__category__slug=category_slug, group__slug=group_slug)
        return queryset


class ProductAttributeListAPIView(ListAPIView):
    serializer_class = AttributeSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Attribute.objects.filter(product__slug=slug).select_related('key', 'value')


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()


