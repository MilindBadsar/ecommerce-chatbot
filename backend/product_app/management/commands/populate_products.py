import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from product_app.models import Category, Product

class Command(BaseCommand):
    help = 'Populates the database with mock e-commerce products and categories.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating categories...")

        categories_data = [
            {'name': 'Electronics', 'description': 'Gadgets, devices, and accessories.'},
            {'name': 'Books', 'description': 'Novels, non-fiction, textbooks.'},
            {'name': 'Textiles', 'description': 'Clothing, fabrics, and home linen.'},
            {'name': 'Home & Kitchen', 'description': 'Appliances, decor, cookware.'},
            {'name': 'Sports & Outdoors', 'description': 'Gear for activities and adventures.'},
            {'name': 'Beauty & Personal Care', 'description': 'Cosmetics, skincare, hygiene products.'},
            {'name': 'Toys & Games', 'description': 'For kids and adults alike.'},
            {'name': 'Automotive', 'description': 'Car parts, accessories, and maintenance.'},
            {'name': 'Groceries', 'description': 'Food and beverage items.'},
            {'name': 'Health & Fitness', 'description': 'Supplements, exercise equipment.'},
        ]

        created_categories = {}
        for data in categories_data:
            category, created = Category.objects.get_or_create(name=data['name'], defaults={'description': data['description']})
            created_categories[category.name] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(f'Category already exists: {category.name}')

        self.stdout.write("Populating products...")

        product_names = {
            'Electronics': ['Smartphone X', 'Noise Cancelling Headphones', 'Smartwatch Pro', 'Laptop Thin & Light', 'Wireless Earbuds', 'Portable Bluetooth Speaker', 'Drone Explorer', 'Gaming Mouse', 'Mechanical Keyboard', 'External SSD'],
            'Books': ['Sci-Fi Thriller', 'Historical Fiction Epic', 'Cooking Masterclass', 'Gardening Guide', 'Self-Help Bestseller', 'Fantasy Saga Vol. 1', 'Mystery Novella', 'Biography of Innovators', 'Poetry Collection', 'Art History Textbook'],
            'Textiles': ['Organic Cotton T-Shirt', 'Linen Bed Sheets', 'Denim Jeans Classic Fit', 'Wool Scarf', 'Silk Pillowcase', 'Microfiber Towel Set', 'Knitted Sweater', 'Waterproof Jacket', 'Yoga Pants', 'Bathrobe Soft Touch'],
            'Home & Kitchen': ['Blender High Power', 'Coffee Maker Drip', 'Smart Light Bulb', 'Vacuum Cleaner Robot', 'Ceramic Mug Set', 'Non-Stick Frying Pan', 'Air Fryer Compact', 'Digital Kitchen Scale', 'Memory Foam Pillow', 'Aromatherapy Diffuser'],
            'Sports & Outdoors': ['Running Shoes Boost', 'Yoga Mat Non-Slip', 'Water Bottle Insulated', 'Camping Tent 2-Person', 'Fitness Tracker', 'Resistance Bands Set', 'Hiking Backpack', 'Cycling Helmet', 'Jump Rope Speed', 'Dumbbell Set Adjustable']
        }

        all_products_created = 0
        for _ in range(150): 
            category_name = random.choice(list(product_names.keys()))
            category_obj = created_categories.get(category_name)

            if not category_obj:
                # Fallback if category not found (shouldn't happen with current logic)
                self.stdout.write(self.style.WARNING(f"Category object not found for {category_name}. Skipping product."))
                continue

            product_name_base = random.choice(product_names[category_name])
            product_suffix = random.randint(100, 999) 
            name = f"{product_name_base} {product_suffix}"
            description = f"High-quality {product_name_base.lower()} with advanced features and durable design."
            price = Decimal(random.uniform(10.00, 500.00)).quantize(Decimal('0.01'))
            stock = random.randint(0, 200)
            

            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'price': price,
                    'category': category_obj,
                    'stock_quantity': stock,
                }
            )
            if created:
                all_products_created += 1
                # self.stdout.write(f'Created product: {name}') # Uncomment for verbose output
            # else:
                # self.stdout.write(f'Product already exists: {name}') # Uncomment for verbose output

        self.stdout.write(self.style.SUCCESS(f'Successfully created {all_products_created} new products.'))
        self.stdout.write(self.style.SUCCESS('Database population complete.'))