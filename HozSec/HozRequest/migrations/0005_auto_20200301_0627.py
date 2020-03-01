# Generated by Django 3.0.3 on 2020-03-01 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HozRequest', '0004_request_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='photo',
        ),
        migrations.AddField(
            model_name='request',
            name='photo_url',
            field=models.CharField(default='/media/empty-avatar.png', max_length=200, verbose_name='/media/'),
            preserve_default=False,
        ),
    ]