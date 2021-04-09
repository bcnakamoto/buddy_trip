# Generated by Django 2.2 on 2021-02-24 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0009_trip_joined_trips'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='joined_trips',
        ),
        migrations.AddField(
            model_name='user',
            name='joined_trips',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='login_app.Trip'),
        ),
    ]