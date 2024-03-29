# Generated by Django 4.0.5 on 2022-08-17 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=30)),
                ('url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=30, unique=True)),
                ('url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('version', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('active', 'Active'), ('shutdown', 'Shutdown'), ('deleted', 'Deleted')], max_length=15)),
                ('heartbeat', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('in-progress', 'In progress'), ('error', 'Error'), ('done', 'Done'), ('unknown', 'Unknown')], max_length=15)),
                ('archive_status', models.CharField(choices=[('unarchived', 'Unarchived'), ('in-progress', 'In progress'), ('pending-check', 'Pending checks'), ('done', 'Done'), ('error', 'Error'), ('to-verify', 'To verify'), ('unknown', 'Unknown'), ('other', 'Other')], default='unarchived', max_length=15)),
                ('url', models.URLField()),
                ('total_size', models.PositiveBigIntegerField(default=0)),
                ('files', models.JSONField(default=dict)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='balchivist.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('frequency', models.CharField(max_length=30)),
                ('mode', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('active', 'Active'), ('disabled', 'Disabled'), ('deleted', 'Deleted')], max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.CharField(max_length=100)),
                ('priority', models.PositiveSmallIntegerField(default=0)),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('running', 'Running'), ('completed', 'Completed'), ('error', 'Error'), ('unknown', 'Unknown')], max_length=15)),
                ('logurl', models.URLField(blank=True)),
                ('arguments', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('node', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='balchivist.node')),
                ('snapshot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='balchivist.snapshot')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('running', 'Running'), ('completed', 'Completed'), ('error', 'Error'), ('unknown', 'Unknown')], max_length=15)),
                ('runner', models.CharField(blank=True, max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('watchlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='balchivist.watchlist')),
            ],
        ),
        migrations.CreateModel(
            name='NodeConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='balchivist.node')),
            ],
        ),
        migrations.AddField(
            model_name='dataset',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='balchivist.family'),
        ),
        migrations.AddConstraint(
            model_name='userpreference',
            constraint=models.UniqueConstraint(fields=('user', 'key'), name='pk_user_key'),
        ),
        migrations.AddConstraint(
            model_name='snapshot',
            constraint=models.UniqueConstraint(fields=('identifier', 'dataset'), name='pk_identifier_dataset'),
        ),
        migrations.AddConstraint(
            model_name='nodeconfig',
            constraint=models.UniqueConstraint(fields=('node', 'key'), name='pk_node_key'),
        ),
        migrations.AddConstraint(
            model_name='dataset',
            constraint=models.UniqueConstraint(fields=('identifier', 'family'), name='pk_name_family'),
        ),
    ]
