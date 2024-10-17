import pytest
from unittest import mock
from django.core.management import call_command

from inventory_app.models import Product

MOCK_XML = """
    <SHOP>
        <SHOPITEM>
            <PRODUCTNAME>Test Product 1</PRODUCTNAME>
            <ITEM_ID>12345</ITEM_ID>
            <URL>https://example.com/product1</URL>
            <MANUFACTURER>Test Brand 1</MANUFACTURER>
        </SHOPITEM>
        <SHOPITEM>
            <PRODUCTNAME>Test Product 2</PRODUCTNAME>
            <ITEM_ID>67890</ITEM_ID>
            <URL>https://example.com/product2</URL>
            <MANUFACTURER>Test Brand 2</MANUFACTURER>
        </SHOPITEM>
    </SHOP>
    """


@pytest.mark.django_db
@mock.patch("requests.get")
def test_import_xml(mock_get):
    """Testuje import XML souboru pomocí mockování HTTP requests"""

    # mockovani obsahu vracenoho z HTTP pozadavku
    mock_get.return_value.content = MOCK_XML

    # spusteni prikazu import_xml
    call_command("import_xml")

    assert Product.objects.count() == 2

    product1 = Product.objects.get(product_id="12345")
    assert product1.name == "Test Product 1"
    assert product1.url == "https://example.com/product1"
    assert product1.brand == "Test Brand 1"
    assert product1.is_active is True

    product2 = Product.objects.get(product_id="67890")
    assert product2.name == "Test Product 2"
    assert product2.url == "https://example.com/product2"
    assert product2.brand == "Test Brand 2"
    assert product2.is_active is True
