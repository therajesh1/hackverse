# Generated by Django 5.1.7 on 2025-03-27 19:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_assessment_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poprogress',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.customuser'),
        ),
    ]
