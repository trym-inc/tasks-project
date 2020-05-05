from django.db import models

from django_choices import DjangoChoices


class Task(models.Model):
    class Category(DjangoChoices):
        cloning = (0, 'Cloning')
        feeding = (1, 'Feeding')
        moving = (2, 'Moving Batch')
        ipm = (3, 'IPM')

    category = models.IntegerField(choices=Category.choices)
    name = models.CharField(max_length=200)
    description = models.TextField()


class Batch(models.Model):
    name = models.CharField(max_length=200)
    tasks = models.ManyToManyField(Task, related_name='batches')
