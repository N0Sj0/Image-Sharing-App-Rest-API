# Generated by Django 2.1 on 2019-01-09 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0014_auto_20190109_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=20),
        ),
    ]
