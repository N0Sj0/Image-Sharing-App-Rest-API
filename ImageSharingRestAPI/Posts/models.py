from django.db import models
from constants import Constants as const
from Users.models import Profile
import django.utils.timezone
# Create your models here.


class Post(models.Model):
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='owner')
    owner_string = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)
    liked_users = models.CharField(max_length=3000)
    date = models.DateTimeField(default=django.utils.timezone.now)

    @property
    def image_url(self):
        return const.BASE_URL + const.post_images_query + self.owner_string + str(self.pk) + ".png/"

    def __str__(self):
        return self.owner_string + str(self.post_id)