import pytest
from django.urls import reverse
from inventory_app.forms import TaskForm


@pytest.mark.django_db
def test_task_valid(client, task_object, login):
    """Testuje validní vytvoření Task metodou POST a kontrolou formuláře."""
    url = reverse("new-task")
    client.force_login(login)

    data = {
        "task": task_object.task,
        "description": task_object.description,
        "is_done": task_object.is_done,
    }

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("tasks")

    form = TaskForm(data)
    assert form.is_valid()

    task_object = form.save()
    assert task_object.task == "Test Task"
    assert task_object.description == "Test Description"
    assert task_object.is_done is False


@pytest.mark.django_db
def test_task_invalid(client, task_object, login):
    """Testuje nevalidní vytvoření Task při chybějícím poli 'task'."""
    url = reverse("new-task")
    client.force_login(login)

    data = {
        "description": task_object.description,
        "is_done": task_object.is_done,
    }

    response = client.post(url, data)
    assert response.status_code == 200

    form = TaskForm(data)
    assert not form.is_valid()
