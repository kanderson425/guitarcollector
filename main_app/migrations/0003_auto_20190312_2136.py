# Generated by Django 2.1.5 on 2019-03-12 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_lastpracticed'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LastPracticed',
            new_name='LastPractice',
        ),
    ]
