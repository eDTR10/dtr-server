# Generated by Django 4.2.16 on 2024-10-21 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('activity_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('fromDate', models.DateField()),
                ('toDate', models.DateField()),
                ('status', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('USERID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
