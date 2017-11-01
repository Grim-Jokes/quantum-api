from django.db import models
from django.conf import settings

# Create your models here.


class AuditableModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(
        'self', null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return f"{self.pk}. {self.name}"


class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=100)
    value = models.DecimalField(decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, null=True)

    def __str__(self):
        return f"{self.description} - {self.value} - {self.date}"
