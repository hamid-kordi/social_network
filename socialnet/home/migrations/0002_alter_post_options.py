# Generated by Django 5.0.2 on 2024-04-06 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('created', 'body')},
        ),
    ]