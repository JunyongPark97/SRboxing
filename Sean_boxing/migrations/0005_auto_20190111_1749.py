# Generated by Django 2.1.1 on 2019-01-11 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sean_boxing', '0004_auto_20190111_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='frame_source',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='box_from_frame', to='Sean_boxing.Frame'),
        ),
    ]