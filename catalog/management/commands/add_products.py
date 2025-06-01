from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add test products to the database"

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(
            name="Декоративная косметика",
            description="Средства для макияжа",
        )

        products = [
            {
                "name": "Тени для век",
                "description": "Палетка из 4-х цветов, коричневая",
                "category": category,
                "price": 1500,
            },
            {
                "name": "Блеск для губ",
                "description": "Блеск для губ, светло-розовый",
                "category": category,
                "price": 1000,
            },
            {
                "name": "Тушь для ресниц",
                "description": "Тушь для ресниц для придания объема и разделения, черная",
                "category": category,
                "price": 1100,
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added product: {product.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Product already exists: {product.name}"))
