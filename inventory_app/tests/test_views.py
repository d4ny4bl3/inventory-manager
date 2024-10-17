import pytest
from django.urls import reverse

from inventory_app.models import Product, Task


@pytest.mark.django_db
def test_index_view_login(client, login):
    """Test, zda přihlášený uživatel má přístup na stránku (200)."""
    client.force_login(login)
    response = client.get(reverse('index'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_index_view_no_login(client):
    """Test, zda nepřihlášený uživatel je přesměrován na login stránku (302)."""
    response = client.get(reverse('index'))
    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_search_view_login(client, login):
    """Test, zda přihlášený uživatel má přístup na stránku (200)."""
    client.force_login(login)
    response = client.get(reverse('search'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_view_no_login(client):
    """Test, zda nepřihlášený uživatel je přesměrován na login stránku (302)."""
    response = client.get(reverse('search'))
    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_new_product_view_post_valid(client, login):
    """Testuje validní POST požadavek pro vytvoření nového produktu."""
    client.force_login(login)

    data = {
        'name': "New Test Product",
        'brand': "Test Brand",
        'product_id': "test_product_id_123",
        'url': "https://example.com/new-product",
        'location': [],
    }

    url = reverse("new-product")
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("products")

    assert Product.objects.filter(product_id="test_product_id_123").exists()


@pytest.mark.django_db
def test_new_product_view_post_invalid(client, login):
    """Testuje nevalidní POST požadavek pro vytvoření nového produktu."""
    client.force_login(login)

    data = {
        'brand': "Test Brand",
        'product_id': "test_product_id_123",
        'url': "https://example.com/new-product",
        'location': [],
    }

    url = reverse("new-product")
    response = client.post(url, data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_new_task_view_post_valid(client, login):
    """Testuje validní POST požadavek pro vytvoření nového úkolu."""
    client.force_login(login)

    data = {
        "task": "Test Task",
        "description": "Test Description",
    }

    url = reverse("new-task")
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("tasks")

    assert Task.objects.filter(task="Test Task").exists()


@pytest.mark.django_db
def test_new_task_view_post_invalid(client, login):
    """Testuje nevalidní POST požadavek pro vytvoření nového úkolu."""
    client.force_login(login)

    data = {
        "description": "Test Description",
    }

    url = reverse("new-task")
    response = client.post(url, data)
    assert response.status_code == 200
