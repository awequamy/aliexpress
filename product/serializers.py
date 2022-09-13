from dataclasses import field
from rest_framework import serializers
from .models import Comments, Product, Favorites
from django.db.models import Avg
from .models import Likes
from django.contrib.auth import get_user_model

User=get_user_model()

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=('title','price','image')
    # def to_representation(self, instance):
    #     repr=super().to_representation(instance)
    #     repr['rating']=instance.reviews.aggregate(Avg('rating'))['rating__avg']

    #     return repr

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
        

    def to_representation(self, instance):
        repr=super().to_representation(instance)
        repr['rating']=instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['reviews']=instance.reviews.count()
        return repr

# class ProductCreateSerializer(serializers.ModelSerializer):
#     # owner = serializers.ReadOnlyField(source='owner.username')
#     # images = RecipeImageSerializer(many=True, read_only=False, required=False)

#     class Meta:
#         model = Product
#         fields = ('title', 'body', 'category', 'preview', 'images')

#     def create(self, validated_data):
#         # print('Validated data: ', validated_data)
#         request = self.context.get('request')
#         # print('FILES', request.FILES)
#         created_post=Product.objects.create(**validated_data)
#         images_data=request.FILES
#         # print(created_post)
#         # print('work',images_data.getlist('images'))
#         # images_object=[PostImages(post=created_post,image=image) for image in images_data.getlist('images')]
#         # PostImages.objects.bulk_create(images_object)
#         return created_post

class LikeSerializer(serializers.ModelSerializer):
    # user=serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model=Likes
        fields=('user',)


class CommentSerilizer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.email')
    class Meta:
        model=Comments
        fields=('user', 'body','product')

class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favorites
        fields=('product',)
    def to_representation(self, instance):
        repr= super().to_representation(instance)
        repr['product']=ProductListSerializer(instance.product).data
        return repr
