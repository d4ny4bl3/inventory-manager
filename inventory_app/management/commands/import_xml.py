import xml.etree.ElementTree as ET
import requests
from django.core.management.base import BaseCommand

from inventory_app.models import Product
from django.utils.text import slugify

from inventory_manager.config import xml_url


class Command(BaseCommand):
    """
    Tento příkaz importuje XML soubor z externí URL.
    Přidá nebo aktualizuje produkty v databazí a deaktivuje produkty, které už nejsou ve feedu.
    """

    help = 'Import XML file'

    def handle(self, *args, **kwargs):

        # stahnuti xml
        try:
            response = requests.get(xml_url)
            response.raise_for_status()  # overeni zda se soubour spravne stahnul
            xml_data = response.content
            self.stdout.write(self.style.SUCCESS('XML import success'))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"XML import failed: {e}"))
            return

        # parsovani xml
        try:
            root = ET.fromstring(xml_data)
        except ET.ParseError as e:
            self.stdout.write(self.style.ERROR(f"XML parsing failed: {e}"))
            return

        # ziskani vsech product_id a ulozeni do mnoziny
        all_products = set(Product.objects.values_list("product_id", flat=True))

        # prochazeni xml a ukladani produktu
        for item in root.findall("SHOPITEM"):
            name = item.find("PRODUCTNAME").text
            product_id = item.find("ITEM_ID").text
            url = item.find("URL").text
            brand = item.find("MANUFACTURER").text

            # ulozeni nebo aktualizace produktu v databazi
            product, created = Product.objects.update_or_create(
                product_id=product_id,
                defaults={
                    "name": name,
                    "brand": brand,
                    "url": url,
                    "slug": slugify(name),
                    "is_active": True
                }
            )

            # odebrani z monoziny produkty, ktere jsou ve feedu
            all_products.discard(product_id)

        deactivated_products = Product.objects.filter(product_id__in=all_products)

        # spusteni funkce deactivate z modelu
        for product in deactivated_products:
            product.deactivate()

        self.stdout.write(self.style.SUCCESS("Successfully imported"))
