# Generated by Django 2.1 on 2018-10-31 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20181031_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(default='ANVANDARNAMN', max_length=20),
            preserve_default=False,
        ),
    ]