# Generated by Django 4.2.16 on 2024-10-22 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
        ('accounts', '0008_alter_useraccount_deptid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='deptid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.department'),
        ),
    ]
