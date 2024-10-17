import pytest
from django.core.exceptions import ValidationError
from inventory_app.models import Room


@pytest.mark.django_db
def test_room_create():
    """Testuje vytvoření Room."""
    room = Room.objects.create(name="Room 1", description="Room 1")
    assert room.name == "Room 1"
    assert room.description == "Room 1"


@pytest.mark.django_db
def test_room_unique():
    """Testuje, jestli je Room name unikátní."""
    Room.objects.create(name="Room 2", description="Room 2")
    room = Room(name="Room 2", description="Room 2")

    with pytest.raises(ValidationError):
        room.clean()


@pytest.mark.django_db
def test_product_create(product_object):
    """Testuje vytvoření Product."""
    product, location1, location2, rack, room = product_object

    assert product.name == "Test product"
    assert product.product_id == "1120245"
    assert product.brand == "Test"
    assert product.location.count() == 2
    assert product.location.first().rack == rack


@pytest.mark.django_db
def test_product_deactivate(product_object):
    """Testuje metodu deactivate - nastavení 'is_active' na False a nakopírování 'location' do 'old_location'."""
    product, location1, location2, rack, room = product_object

    assert product.is_active is True
    assert product.old_location == ""
    product.deactivate()
    assert product.is_active is False
    locations = f"{location1}, {location2}"
    assert product.old_location == locations
