# Generated by Django 2.1.7 on 2019-03-09 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ohsiha_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Juna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tunnus', models.CharField(max_length=100)),
                ('junaAjossa', models.CharField(max_length=10)),
                ('junaKohdeasema', models.CharField(max_length=10)),
                ('junaLahtoasema', models.CharField(max_length=10)),
                ('junaLahtoaika', models.DateTimeField()),
                ('junaLahtoaikaEnnuste', models.DateTimeField()),
                ('junaLahtoaikaEro', models.DateTimeField()),
                ('junaLahtoaikaTod', models.DateTimeField()),
                ('junaPeruttu', models.CharField(max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Z',
        ),
    ]
