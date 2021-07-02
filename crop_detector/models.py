from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Image(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    image_name = models.CharField(max_length=100, default="image")
    images = models.ImageField(upload_to="img/%y", null=True, blank=True)
    plant_name = models.CharField(max_length=100, default="NULL")
    plant_health = models.CharField(max_length=100, default="NULL")
    longitude = models.DecimalField(
        max_digits=22, decimal_places=16, default=Decimal(0))
    latitude = models.DecimalField(
        max_digits=22, decimal_places=16, default=Decimal(0))
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.image_name

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.images.storage, self.images.path
        # Delete the model before the file
        super(Image, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
