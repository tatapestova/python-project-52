# Generated by Django 4.2.3 on 2023-07-31 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_taskslabels_tasks_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Имя'),
        ),
    ]