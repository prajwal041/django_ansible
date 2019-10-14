from django.db import models


# Create your models here.

class Domain(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, primary_key=True, unique=True)
    favcolor = models.CharField(max_length=255, blank=False, null=False)
    pet = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'dom'