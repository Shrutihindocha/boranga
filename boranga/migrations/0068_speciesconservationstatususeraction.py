# Generated by Django 3.2.12 on 2022-08-30 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boranga', '0067_auto_20220826_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeciesConservationStatusUserAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('who', models.IntegerField()),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('what', models.TextField()),
                ('species_conservation_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_logs', to='boranga.speciesconservationstatus')),
            ],
            options={
                'ordering': ('-when',),
            },
        ),
    ]