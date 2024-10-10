# management/commands/load_data.py
from django.core.management.base import BaseCommand
from main.models import Product, Category
import json

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
                Category.objects.get_or_create(
                    category_name_ru=category_name_ru,
                    category_name_en=category_name_en,
                    defaults={'photo': photo}
                )

            except KeyError as e:
                self.stdout.write(self.style.ERROR(f"Missing key: {e} in item: {cat_data}"))

        # Загрузка продуктов
        with open('food.json', 'r', encoding='utf-8') as file:
            products = json.load(file)

        for prod_data in products:
            try:
                # Получаем категорию по ID
                category = Category.objects.get(id=prod_data.pop('category_id'))

                # Удаляем поле product_id и описания, если они есть
                prod_data.pop('product_id', None)
                prod_data.pop('description_ru', None)  # Удаляем description_ru
                prod_data.pop('description_en', None)  # Удаляем description_en

                # Преобразуем цену в строку
                price_str = prod_data.pop('price').replace(' ', '')
                price = price_str  # оставляем как текст

                # Извлекаем имя файла для фото
                photo = prod_data.pop('photo', None)
                if photo:
                    photo = f"{photo}"

                # Создаем продукт
                Product.objects.create(
                    category=category,
                    price=price,
                    photo=photo,
                    **prod_data
                )

                self.stdout.write(self.style.SUCCESS(f"Product '{prod_data['name_en']}' created successfully"))

            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Category with id {prod_data['category_id']} does not exist"))
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Invalid data format in product: {prod_data}. Error: {e}"))

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
