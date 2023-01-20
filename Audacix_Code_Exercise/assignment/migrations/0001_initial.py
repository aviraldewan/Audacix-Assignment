# Generated by Django 4.0.4 on 2023-01-19 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_state', models.CharField(max_length=10)),
                ('word_state', models.CharField(max_length=10)),
                ('attempts_used', models.IntegerField()),
                ('attempts_left', models.IntegerField()),
            ],
        ),
    ]
