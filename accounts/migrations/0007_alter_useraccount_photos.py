# Generated by Django 4.2.16 on 2024-10-22 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_useraccount_photos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='photos',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
    ]
