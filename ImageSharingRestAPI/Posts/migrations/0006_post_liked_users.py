# Generated by Django 2.1 on 2018-11-27 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0005_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='liked_users',
            field=models.CharField(default='', max_length=3000),
            preserve_default=False,
        ),
    ]
