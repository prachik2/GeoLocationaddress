from django.db import models


# Create your models here.
class Address(models.Model):
    address_1 = models.CharField(max_length=256)
    address_2 = models.CharField(max_length=256, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=3)
    longitude = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        return "{}--{},{}".format(self.address_1, self.longitude, self.longitude)

    class Meta:
        db_table = 'address_table'
