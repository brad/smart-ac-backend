# Generated by Django 2.1.7 on 2019-06-02 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_editable_true'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='firmware_version',
            field=models.CharField(default='v1.0.0', max_length=32),
            preserve_default=False,
        ),
    ]