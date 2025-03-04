# Generated by Django 3.2.18 on 2023-05-11 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DoctorApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=400)),
                ('available_from_time', models.TimeField()),
                ('available_till_time', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
