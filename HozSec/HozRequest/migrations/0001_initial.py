# Generated by Django 3.0.3 on 2020-02-29 07:50
import HozRequest.models as hz_m
from django.db import migrations, models



class Migration(migrations.Migration):
    dependencies = [
    ]
    initial = True

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.TextField()),
                ('ruleset', models.TextField(validators=[hz_m.user_ruleset_validator])),
                ('name', models.CharField(default='', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField()),
                ('private', models.BooleanField(default=True)),
                ('problem_text', models.TextField(max_length=5000)),
                ('resolved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default='user', on_delete=models.deletion.DO_NOTHING, to='HozRequest.User')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('message_text', models.TextField(max_length=500)),
                ('request', models.ForeignKey(on_delete=models.deletion.DO_NOTHING, to='HozRequest.Request')),
                ('user', models.ForeignKey(on_delete=models.deletion.DO_NOTHING, to='HozRequest.User')),
            ],
        ),
    ]
