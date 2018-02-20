from django.db import models
from django.conf import settings


class AuditableModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100)
    limit = models.DecimalField(decimal_places=2, max_digits=7, default=0)

    # Order relative within the section
    order = models.IntegerField()

    def __str__(self):
        return f"{self.pk}. {self.name}"


class Description(models.Model):
    """
    Track all of the transaction descriptions here to avoid duplicate entries
    """
    name = models.CharField(max_length=100)


class DescriptionInfo(models.Model):
    """
    Track each description per category.
    Example: Costco
    I spend 70 dollars for gas on week 1.
    So the min AND max get set to 70.00.
    On Week 2, I spend 75 on gas.
    Now the min is 70, and the max is 75.
    If on Week 3 I spend 73.25 then there is a 100% chance that this purchase
    was for gas.
    """
    category = models.ForeignKey(Category)
    description = models.ForeignKey(
        Description,
        related_name="description_info"
    )
    max = models.DecimalField(decimal_places=2, max_digits=8)
    min = models.DecimalField(decimal_places=2, max_digits=8)


class Transaction(models.Model):
    date = models.DateField()
    name = models.ForeignKey(Description)
    value = models.DecimalField(decimal_places=2, max_digits=8)
    category = models.ForeignKey(Category, null=True)

    def __str__(self):
        return f"{self.name_id} - {self.value} - {self.date}"
