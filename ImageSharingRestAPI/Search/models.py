from django.db import models

# Create your models here.


class SearchNode(models.Model):
    val = models.CharField(max_length=50)
    usernames = models.CharField(max_length=3000)