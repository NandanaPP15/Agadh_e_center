from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    documents = models.JSONField()
    fee = models.DecimalField(max_digits=6, decimal_places=2)
    processing_time = models.CharField(max_length=50)

    def __str__(self):
        return self.name
