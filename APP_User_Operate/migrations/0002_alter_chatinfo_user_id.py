# Generated by Django 4.1.7 on 2023-03-31 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP_User_Operate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatinfo',
            name='user_id',
            field=models.IntegerField(help_text='user_id'),
        ),
    ]
