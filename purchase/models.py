from django.db import models
from user.models import User
from myapp.models import Product

from django.utils.translation import gettext_lazy as _

# Create your models here.
class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PD", _("Pending")
        COMPLETED = "CP", _("Completed")
        CANCELED = "CC", _("Canceled")
    order_id = models.AutoField(primary_key=True, db_column='order_id')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order_status = models.CharField(
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING, # default value
    )


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True, db_column='order_item_id')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    amount = models.PositiveIntegerField()


class Transaction(models.Model):
    class StatusChoices(models.TextChoices):
        COMPLETED = "CP", _("Completed")
        CANCELED = "CC", _("Canceled")
    transaction_id = models.AutoField(primary_key=True, db_column='transaction_id')
    order_item = models.ForeignKey(OrderItem, on_delete=models.DO_NOTHING)
    transaction_status = models.CharField(
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.COMPLETED,
    )