# from itertools import product
from itertools import product
from urllib import response
from . import serializers
from .models import Product
from rest_framework import permissions, response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rating.serializers import ReviewSerializer
from multiprocessing import context
from rest_framework import permissions, response
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rating.serializers import ReviewSerializer
from . import serializers
from . models import *
from rest_framework.decorators import action
from .serializers import *
from . import serializers
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import CommentSerilizer



class StandartResultsPagination(PageNumberPagination):
    page_size=3
    page_query_param='page'
    max_page_size=1000
    


class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    filter_backends=(DjangoFilterBackend,SearchFilter)
    filterset_fields=('category',)
    search_fields=('title',)
    pagination_class=StandartResultsPagination
    
    def get_serializer_class(self):
        if self.action=='list':
            return serializers.ProductListSerializer
        return serializers.ProductDetailSerializer

    @action(['GET','POST'],detail=True)
    def reviews(self,request,pk=None):
        product=self.get_object()
        if request.method=='GET':
            reviews=product.reviews.all()
            serializer=ReviewSerializer(reviews,many=True).data
            return response.Response(serializer,status=200)
        data=request.data
        serializer=ReviewSerializer(data=data,context={'request':request,'product':product})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data,status=201)
    
    @action(['GET'],detail=True)
    def comments(self,request,pk):
        product=self.get_object()
        comments=product.comments.all()
        serializer=serializers.CommentSerilizer(comments,many=True)
        return Response(serializer.data,status=200)
    
    # api/v1/posts/<id>/add_to_liked/
    @action(['POST'],detail=True)
    def add_to_liked(self,request,pk):
        product=self.get_object()
        if request.user.liked.filter(product=product).exists():
            # request.user.liked.filter(post=post).delete()
            return Response('Вы уже лайкнули этот продукт!!!!!',status=400)
        Likes.objects.create(product=product,user=request.user)
        return Response('Вы поставили лайк', status=201)

    #api/v1/posts/<id>/remove_from_liked
    @action(['POST'],detail=True)
    def remove_from_liked(self,request,pk):
        product=self.get_object()
        if not request.user.liked.filter(product=product).exists():
            return Response('Вы не лайкали этот продукт!!!',status=400)
        request.user.liked.filter(product=product).delete()
        return Response('Вы убрали ваш лайк',status=204)

    #api/v1/posts/<id>/get_likes
    @action(['GET'],detail=True)
    def get_likes(self,request,pk):
        product=self.get_object()
        likes=product.likes.all()
        serializer=serializers.LikeSerializer(likes,many=True)
        return Response(serializer.data,status=200)

    @action(['POST'],detail=True,)
    def favorite_action(self,request,pk):
        product=self.get_object()
        if request.user.favorites.filter(product=product).exists():
            request.user.favorites.filter(product=product).delete()
            return Response('Убрали из избранных',status=204)
        Favorites.objects.create(product=product,user=request.user)
        return Response('Добавлено в изрбанное',status=201)

class CommentListCreateView(generics.ListCreateAPIView):
    queryset=Comments.objects.all()
    serializer_class=serializers.CommentSerilizer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class  CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comments.objects.all()
    serializer_class=CommentSerilizer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

    
 