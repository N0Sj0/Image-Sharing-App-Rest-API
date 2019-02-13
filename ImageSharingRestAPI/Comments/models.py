from django.db import models
from Posts.models import Post
from Users.models import Profile
# Create your models here.


class Comment(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='owner')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

