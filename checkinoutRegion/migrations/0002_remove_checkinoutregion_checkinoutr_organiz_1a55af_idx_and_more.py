# Generated by Django 4.2.8 on 2025-01-28 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkinoutRegion', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='checkinoutregion',
            name='checkinoutR_organiz_1a55af_idx',
        ),
        migrations.RemoveIndex(
            model_name='checkinoutregion',
            name='checkinoutR_USERID__906ca7_idx',
        ),
        migrations.RemoveField(
            model_name='checkinoutregion',
            name='organization',
        ),
    ]
