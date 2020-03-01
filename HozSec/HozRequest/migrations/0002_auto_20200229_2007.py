# Generated by Django 3.0.3 on 2020-02-29 20:07

import HozRequest.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HozRequest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.TextField()),
                ('ruleset', models.TextField(validators=[HozRequest.models.user_ruleset_validator])),
            ],
        ),
        migrations.RemoveField(
            model_name='request',
            name='long_text',
        ),
        migrations.RemoveField(
            model_name='request',
            name='short_text',
        ),
        migrations.RemoveField(
            model_name='request',
            name='title',
        ),
        migrations.AddField(
            model_name='request',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='request',
            name='private',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='request',
            name='problem_text',
            field=models.TextField(default='', max_length=5000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='request',
            name='theme',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('message_text', models.TextField(max_length=500)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='HozRequest.Request')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='HozRequest.User')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='HozRequest.User'),
            preserve_default=False,
        ),
    ]
