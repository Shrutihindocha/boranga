# Generated by Django 3.2.20 on 2023-09-26 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boranga', '0178_rename_name_observerdetail_observer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observerdetail',
            name='occurrence_report',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observer_detail', to='boranga.occurrencereport'),
        ),
    ]
