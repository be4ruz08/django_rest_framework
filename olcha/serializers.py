from django.db.models import Avg
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from olcha.models import Category, Group, Product, Image, Attribute
from rest_framework_simplejwt.tokens import RefreshToken


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
    category_name = serializers.CharField(source='group.category.title')
    group_name = serializers.CharField(source='group.title')
    is_liked = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    comment_info = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, instance):
        attrs = instance.attributes.all().values('key__name', 'value__name')

        product_attributes = [
            {
                'attribute_name': attribute['key__name'],
                'attribute_value': attribute['value__name']
            }
            for attribute in attrs
        ]
        return product_attributes

    def get_comment_info(self, obj):
        return obj.comments.all().values('message', 'rating', 'user__username')

    def get_all_images(self, instance):
        request = self.context.get('request', None)
        images = instance.images.all().order_by('-is_primary', '-id')
        all_images = []
        for image in images:
            all_images.append(request.build_absolute_uri(image.image.url))

        return all_images

    def get_avg_rating(self, obj):
        avg_rating = obj.comments.aggregate(avg=Avg('rating'))['avg']
        print(avg_rating)
        return round(avg_rating, 1) if avg_rating is not None else 0

    def get_image(self, obj):
        image = obj.images.filter(is_primary=True).first()
        if image:
            image_url = image.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url)

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user in obj.is_liked.all():
                return True
        return False

    class Meta:
        model = Product
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source='key.name')
    value = serializers.CharField(source='value.name')

    class Meta:
        model = Attribute
        fields = ['key', 'value']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    first_name = serializers.CharField(max_length=125, required=False)
    last_name = serializers.CharField(max_length=125, required=False)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, write_only=True)
    password2 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already taken")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


