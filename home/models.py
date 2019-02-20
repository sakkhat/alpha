from django.db import models
from space.models import Space

class Trends(models.Model):
	space = models.OneToOneField(Space, on_delete=models.CASCADE)
