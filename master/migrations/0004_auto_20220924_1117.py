# Generated by Django 3.2.15 on 2022-09-24 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_ticket_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='user_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='user_phone_number',
            new_name='phone_number',
        ),
    ]
