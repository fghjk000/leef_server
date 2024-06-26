# Generated by Django 5.0.4 on 2024-04-20 07:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('leef', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('price', models.IntegerField(default=0)),
                ('category', models.CharField(max_length=10)),
                ('image', models.TextField()),
                ('choice', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leef.user')),
            ],
        ),
    ]
