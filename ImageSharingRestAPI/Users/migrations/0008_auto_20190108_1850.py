# Generated by Django 2.1 on 2019-01-08 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_remove_profile_profile_pic_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id',
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
