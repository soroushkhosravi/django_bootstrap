# Generated by Django 4.2.3 on 2023-09-22 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_choice_question_alter_question_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='choice',
            table='choice',
        ),
    ]
