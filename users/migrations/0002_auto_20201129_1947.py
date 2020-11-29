# Generated by Django 3.1.3 on 2020-11-29 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.CreateModel(
            name='UserIdentity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, upload_to='')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=15)),
                ('birth_date', models.DateTimeField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]