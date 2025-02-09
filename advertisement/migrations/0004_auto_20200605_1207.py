# Generated by Django 3.0.6 on 2020-06-05 12:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0003_offer_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='display_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='offer',
            name='display_period',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='offer',
            name='category',
            field=models.CharField(choices=[('brak', 'brak'), ('praca - zatrudnie', 'praca - zatrudnie'), ('prace - poszukuje', 'prace - poszukuje'), ('elektronika - kupie', 'elektronika - kupie'), ('elektronika - sprzedam', 'elektronika - sprzedam'), ('usługi - zlece', 'usługi - zlece'), ('usługi - wykonam', 'usługi - wykonam'), ('dom - kupie', 'dom - kupie'), ('dom - sprzedam', 'dom - sprzedam')], default='brak', max_length=30),
        ),
    ]
