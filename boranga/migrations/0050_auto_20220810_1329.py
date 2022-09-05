# Generated by Django 3.2.12 on 2022-08-10 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boranga', '0049_auto_20220809_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitydistribution',
            name='community_original_area',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='communitydistribution',
            name='community_original_area_accuracy',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='communitydistribution',
            name='community_original_area_reference',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='conservationthreat',
            name='threat_agent',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='common_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='name_currency',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='processing_status',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='scientific_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='speciesconservationattributes',
            name='average_lifespan',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='speciesconservationattributes',
            name='fauna_reproductive_capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='speciesconservationattributes',
            name='generation_length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='speciesconservationattributes',
            name='time_to_maturity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='speciesdistribution',
            name='area_of_occupancy',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='speciesdistribution',
            name='department_file_numbers',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='speciesdistribution',
            name='extent_of_occurrences',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='speciesdistribution',
            name='number_of_iucn_locations',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='speciesdistribution',
            name='number_of_occurrences',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='taxonomy',
            name='taxon',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='taxonomy',
            name='taxon_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]