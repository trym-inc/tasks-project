import pytest
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from tasks.models import Task


@pytest.mark.django_db
class TestTaskViewSet:
    task_list_url = reverse_lazy('tasks:task-list')

    @pytest.fixture(autouse=True)
    def init(self):
        self.api_cli = APIClient()

    def test_create_task(self):
        category = Task.Category.moving
        name = 'category test name'
        description = 'test description'

        task_data = {
            'category': category.key,
            'name': name,
            'description': description,
        }

        response = self.api_cli.post(self.task_list_url, data=task_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['name'] == name
        assert response.data['description'] == description
        assert response.data['category'] == category.key
        assert response.data['category_display'] == category.label

        task = Task.objects.first()

        assert task.category == category.key
        assert task.name == name
        assert task.description == description

    def test_list_tasks(self):
        category = Task.Category.moving.key
        name = 'category test name'
        description = 'test description'

        task = Task.objects.create(
            name=name,
            category=category,
            description=description,
        )

        response = self.api_cli.get(self.task_list_url)

        data = response.json()

        assert len(data) == 1
        assert data[0]['id'] == task.id
        assert data[0]['category'] == task.category
        assert data[0]['category_display'] == Task.Category(task.category).label
        assert data[0]['description'] == task.description

