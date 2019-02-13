from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from constants import Constants as const
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    firstname = models.CharField(max_length=15)
    lastname = models.CharField(max_length=20)
    bio = models.CharField(max_length=150)
    follows_string = models.CharField(max_length=3000)
    followers_string = models.CharField(max_length=3000)
    follows_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)

    @property
    def profile_pic_url(self):
        return const.BASE_URL + const.profile_pics_query + self.username + ".png/"

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

