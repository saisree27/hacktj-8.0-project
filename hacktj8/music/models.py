from django.db import models

# Create your models here.

class File(models.Model):
    filename = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='files/', blank=True, null=True)