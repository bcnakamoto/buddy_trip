# Generated by Django 2.2 on 2021-02-24 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0011_auto_20210224_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='joined_trips',
            new_name='joiner',
        ),
    ]
