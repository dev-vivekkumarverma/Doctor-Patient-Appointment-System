# Generated by Django 3.2.18 on 2023-06-02 06:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DoctorApp', '0005_doctoreductaionaldetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctoreductaionaldetails',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
