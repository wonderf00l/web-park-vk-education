# Generated by Django 4.2 on 2023-06-17 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0002_alter_answer_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='correctness_degree',
        ),
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]
