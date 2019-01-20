# Generated by Django 2.1.5 on 2019-01-19 06:54

from django.db import migrations, models
import django.db.models.deletion
import tournament.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('award', models.CharField(choices=[('A', 'Keen eyes on their stuff'), ('B', 'Outstanding Performances'), ('C', 'Race for the initial markets'), ('D', 'Eggs in multiple baskets'), ('E', 'Commercial Meteorology Experiment'), ('F', 'Mind Games')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FFaMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('location', models.CharField(choices=[('M', 'Mars'), ('C', 'Ceres'), ('I', 'Io')], max_length=6)),
                ('notes', models.CharField(default='', max_length=1024)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OvOMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('location', models.CharField(choices=[('M', 'Mars'), ('C', 'Ceres'), ('I', 'Io')], max_length=6)),
                ('notes', models.CharField(default='', max_length=1024)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('name', models.CharField(max_length=60)),
                ('discordname', models.CharField(max_length=60, null=True)),
                ('bracket', models.IntegerField()),
                ('stars', models.IntegerField()),
                ('preference', models.IntegerField(validators=[tournament.models.validate_preference])),
                ('availability', models.IntegerField(validators=[tournament.models.validate_availability])),
                ('will_ffa', models.BooleanField()),
                ('will_1v1', models.BooleanField()),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='tournament.Team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2', to='tournament.Team')),
                ('team3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team3', to='tournament.Team')),
                ('team4', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team4', to='tournament.Team')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Team'),
        ),
        migrations.AddField(
            model_name='ovomatch',
            name='player1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p1', to='tournament.Player'),
        ),
        migrations.AddField(
            model_name='ovomatch',
            name='player2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p2', to='tournament.Player'),
        ),
        migrations.AddField(
            model_name='ovomatch',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tournament.Player'),
        ),
        migrations.AddField(
            model_name='ffamatch',
            name='player1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1', to='tournament.Player'),
        ),
        migrations.AddField(
            model_name='ffamatch',
            name='player2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player2', to='tournament.Player'),
        ),
        migrations.AddField(
            model_name='ffamatch',
            name='player3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player3', to='tournament.Player'),
        ),
        migrations.AddField(
            model_name='ffamatch',
            name='player4',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player4', to='tournament.Player'),
        ),
        migrations.AddField(
            model_name='ffamatch',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tournament.Player'),
        ),
        migrations.AddField(
            model_name='award',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.FFaMatch'),
        ),
        migrations.AddField(
            model_name='award',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Player'),
        ),
    ]
