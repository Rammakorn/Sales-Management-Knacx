from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True, db_column='product_id')
    product_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)