from django.core.management.base import BaseCommand
from main.models import Product, Category
import json
import os


class Command(BaseCommand):
    help = 'Loads product and category data from JSON files'

    def handle(self, *args, **kwargs):
        # Загрузка категорий
        with open('categories.json', 'r', encoding='utf-8') as file:
            categories = json.load(file)

        for cat_data in categories:
            try:
                category_name_ru = cat_data['category_name_ru']
                category_name_en = cat_data['category_name_en']
                photo = cat_data.get('photo', None)

                # Создание или получение категории
                category, created = Category.objects.get_or_create(
                    category_name_ru=category_name_ru,
                    category_name_en=category_name_en,
                    defaults={'photo': photo}
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Category '{category_name_en}' created successfully"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Category '{category_name_en}' already exists"))

            except KeyError as e:
                self.stdout.write(self.style.ERROR(f"Missing key: {e} in item: {cat_data}"))

        # Загрузка продуктов
        with open('food.json', 'r', encoding='utf-8') as file:
            products = json.load(file)

        for prod_data in products:
            try:
                # Получаем категорию по ID
                category = Category.objects.get(id=prod_data.pop('category_id'))

                # Удаляем ненужные поля, если они есть
                prod_data.pop('product_id', None)

                # Извлекаем описание с дефолтным значением
                description_ru = prod_data.pop('description_ru', '')
                description_en = prod_data.pop('description_en', '')

                # Оставляем цену как строку
                price = prod_data.pop('price', '')

                # Обновляем путь к фотографии
                photo_filename = prod_data.get('photo')
                if photo_filename:
                    prod_data['photo'] = os.path.join('', photo_filename)

                # Создаем продукт, избегая дублирования полей
                Product.objects.create(
                    category=category,
                    price=price,
                    description_ru=description_ru,
                    description_en=description_en,
                    **prod_data
                )

                self.stdout.write(
                    self.style.SUCCESS(f"Product '{prod_data.get('name_en', 'Unnamed')}' created successfully"))

            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Category with id {prod_data['category_id']} does not exist"))
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Invalid data format in product: {prod_data}. Error: {e}"))

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
