# Generated by Django 4.2.16 on 2024-10-11 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkinout', '0002_rename_userid_checkinout_uid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkinout',
            old_name='UID',
            new_name='USERID',
        ),
    ]
