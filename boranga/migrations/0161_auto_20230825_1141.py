# Generated by Django 3.2.20 on 2023-08-25 03:41

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('boranga', '0160_merge_20230810_0925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='habitatcondition',
            old_name='completely_dehydrated',
            new_name='completely_degraded',
        ),
        migrations.RenameField(
            model_name='habitatcondition',
            old_name='dehydrated',
            new_name='degraded',
        ),
        migrations.AlterField(
            model_name='habitatcomposition',
            name='land_form',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(4, 'BushLand'), (3, 'Costline'), (1, 'Dessert'), (2, 'Mountain')], max_length=250, null=True),
        ),
    ]
