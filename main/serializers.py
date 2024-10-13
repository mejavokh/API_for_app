# serializers.py
from rest_framework import serializers
from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name_ru', 'name_en', 'price', 'photo', 'description_ru', 'description_en']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name_ru', 'category_name_en', 'photo']
