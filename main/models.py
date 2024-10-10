from django.db import models


class Category(models.Model):
    category_name_ru = models.CharField(max_length=255)
    category_name_en = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.category_name_en


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    price = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name_en
