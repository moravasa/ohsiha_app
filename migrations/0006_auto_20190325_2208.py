# Generated by Django 2.1.7 on 2019-03-25 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ohsiha_app', '0005_auto_20190325_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='juna',
            name='junaPeruttu',
            field=models.CharField(max_length=10, null=True),
        ),
    ]