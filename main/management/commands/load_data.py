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
                photo = cat_data.get('photo')

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
                # Проверка наличия category_id
                category_id = prod_data.get('category_id')
                if category_id is None:
                    self.stdout.write(self.style.ERROR(f"Missing 'category_id' in product: {prod_data}"))
                    continue

                # Получаем категорию
                category = Category.objects.get(id=category_id)

                # Преобразуем цену (если не пустая)
                price_str = prod_data.get('price', '').replace(' ', '') or None

                # Удаляем лишние поля
                product_fields = {k: v for k, v in prod_data.items()
                                  if k not in ['category_id', 'product_id', 'price', 'photo', 'description_ru', 'description_en']}

                photo = prod_data.get('photo')
                description_ru = prod_data.get('description_ru')
                description_en = prod_data.get('description_en')

                # Создаем продукт
                Product.objects.create(
                    category=category,
                    price=price_str,
                    photo=photo,
                    description_ru=description_ru,
                    description_en=description_en,
                    **product_fields  # Передаем остальные поля
                )

                self.stdout.write(self.style.SUCCESS(f"Product '{prod_data.get('name_en', 'Unnamed')}' created successfully"))

            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Category with id {category_id} does not exist"))
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Invalid data format in product: {prod_data}. Error: {e}"))

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
