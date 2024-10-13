from django.db import models


class Category(models.Model):
    category_name_ru = models.CharField(max_length=255)
    category_name_en = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.category_name_en


# models.py
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    price = models.CharField(max_length=50, null=True, blank=True)  # Разрешаем NULL и пустые значения
    photo = models.ImageField(upload_to='', null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name_en

