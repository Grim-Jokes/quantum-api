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
    limit = models.DecimalField(decimal_places=2, max_digits=7, default=0)

    # Order relative within the parent
    order = models.IntegerField()

    def __str__(self):
        return f"{self.pk}. {self.name}"


class Description(models.Model):
    """
    Track all of the transaction descriptions here to avoid duplicate entries
    """
    name = models.CharField(max_length=100)


class Transaction(models.Model):
    date = models.DateField()
    name = models.ForeignKey(Description)
    value = models.DecimalField(decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, null=True)

    def __str__(self):
        return f"{self.name_id} - {self.value} - {self.date}"
