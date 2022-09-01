from django.shortcuts import render

from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from . import serializers
from . models import Category


class CategoryViewSet(ModelViewSet):
    queryset=Category.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = serializers.CategoryListSerializer


    # def get_serializer_class(self):
    #     if self.action=='list':
    #         return serializers.CategoryListSerializer

    #     return serializers.CategoryDetailSerializer
