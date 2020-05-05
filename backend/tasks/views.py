from rest_framework.viewsets import ModelViewSet

from tasks.models import Batch, Task
from tasks.serializers import TaskSerializer, BatchSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class BatchViewSet(ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

