# Generated by Django 2.2.16 on 2021-12-16 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('authtoken', '0003_tokenproxy'),
        ('reviews', '0004_auto_20211216_1637'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AnonymousUser',
        ),
    ]