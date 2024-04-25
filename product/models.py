from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=10)
    image = models.TextField()
    user = models.ForeignKey("leef.User", on_delete=models.CASCADE)
    choice = models.BooleanField(default=False)

    class Meta:
        app_label = "product"
