# Generated by Django 4.0.4 on 2023-04-15 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrap_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addressuser',
            name='id',
        ),
        migrations.AddField(
            model_name='addressuser',
            name='aid',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
