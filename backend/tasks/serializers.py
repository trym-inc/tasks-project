from rest_framework import serializers

from tasks.models import Task, Batch


class TaskSerializer(serializers.ModelSerializer):
    category_display = serializers.SerializerMethodField(source='category')

    def get_category_display(self, task):
        return Task.Category(task.category).label

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'category',
            'category_display',
            'description',
        ]


class BatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Batch
        fields = [
            'id',
            'name',
        ]

