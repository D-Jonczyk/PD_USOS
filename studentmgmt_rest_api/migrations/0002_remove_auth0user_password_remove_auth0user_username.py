# Generated by Django 4.2.2 on 2023-06-10 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentmgmt_rest_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auth0user',
            name='password',
        ),
        migrations.RemoveField(
            model_name='auth0user',
            name='username',
        ),
    ]
