# Generated by Django 3.2.6 on 2021-09-03 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210902_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time',
            field=models.TimeField(auto_now=True, null=True),
        ),
    ]
