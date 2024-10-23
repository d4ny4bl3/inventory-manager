import pytest
from django.contrib.auth.models import User
from inventory_app.models import Task, Room, Rack, Location, Product


@pytest.fixture
def login():
    """Vytváří a vrací superuživatele admin."""
    return User.objects.create_superuser(username="admin", password="admin", email="admin@admin.com")


@pytest.fixture
def task_object():
    """Vytváří a vrací objekt Task."""
    return Task.objects.create(task="Test Task", description="Test Description", is_done=False)


@pytest.fixture
def product_object():
    """Vytváří a vrací objekt Product s jeho vztahy - Location, Rack, Room."""
    room = Room.objects.create(name="Room 1", description="Room 1")
    assert room.name == "Room 1"

    rack = Rack.objects.create(room=room, number=1, total_shelves=3)
    assert rack.room == room

    location1 = Location.objects.create(rack=rack, shelf=1)
    assert location1.rack == rack
    assert location1.shelf == 1

    location2 = Location.objects.create(rack=rack, shelf=2)
    assert location2.rack == rack
    assert location2.shelf == 2

    product = Product.objects.create(
        name="Test product",
        brand="Test",
        product_id="1120245",
        old_location="",
        url="https://test.com",
        is_active=True,
        is_check=True,
        slug="test-product"
    )
    product.location.set([location1, location2])

    return product, location1, location2, rack, room
