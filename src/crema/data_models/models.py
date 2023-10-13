from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        """Meta class for the model."""
        db_table = "book"


class Cook(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        """Meta class for the model."""
        db_table = "cook"