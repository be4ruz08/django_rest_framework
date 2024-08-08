from rest_framework import generics
from rest_framework.generics import ListAPIView

from olcha.models import Product
from olcha.serializers import ProductModelSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductModelSerializer

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        group_slug = self.kwargs.get('group_slug')

        if category_slug and group_slug:
            queryset = Product.objects.filter(group__category__slug=category_slug, group__slug=group_slug)
        else:
            queryset = Product.objects.all()

        return queryset


