# Generated by Django 2.1.1 on 2019-01-16 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sean_boxing', '0006_auto_20190114_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anchor',
            name='work_user',
        ),
    ]
