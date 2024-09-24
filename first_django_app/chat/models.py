from django.db import models
from django.db import DateField
from datetime import date

# Create your models here.
class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = DateField(default=date.today)