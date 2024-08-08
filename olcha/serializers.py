from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from olcha.models import Category, Group, Product


class CategoryModelSerializer(ModelSerializer):
    image = serializers.ImageField(max_length=None)
    group_count = serializers.SerializerMethodField()

    def get_group_count(self, obj):
        return obj.groups.count()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'image', 'group_count']


class GroupModelSerializer(ModelSerializer):
    # categories = CategoryModelSerializer(read_only=True)
    category_slug = serializers.SlugField(source='category.slug')
    category_title = serializers.CharField(source='category.title')
    full_image_url = serializers.SerializerMethodField(method_name='foo')

    def foo(self, obj):
        image_url = obj.image.url
        request = self.context.get('request')
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Group
        exclude = ('image', )


class ProductModelSerializer(ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()
    primary_image = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'discount', 'group', 'is_liked', 'average_rating',
                  'discounted_price', 'primary_image']

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user in obj.is_liked.all()
        return False

