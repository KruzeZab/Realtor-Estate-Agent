# Generated by Django 3.0.8 on 2020-07-11 06:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Realtor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('description', models.TextField()),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('website', models.CharField(max_length=60, unique=True)),
                ('company_assoicated', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('hire_date', models.DateTimeField(blank=True, db_index=True, default=datetime.datetime.now)),
            ],
        ),
    ]
