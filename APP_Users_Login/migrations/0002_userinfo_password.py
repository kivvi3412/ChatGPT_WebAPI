# Generated by Django 4.1.7 on 2023-03-30 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP_Users_Login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='password',
            field=models.CharField(blank=True, help_text='password', max_length=200),
        ),
    ]
