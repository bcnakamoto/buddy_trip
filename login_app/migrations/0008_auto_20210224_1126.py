# Generated by Django 2.2 on 2021-02-24 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0007_auto_20210222_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dest', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('plan', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='login_app.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='poster',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]