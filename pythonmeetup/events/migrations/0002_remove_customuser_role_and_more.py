# Generated by Django 4.2.16 on 2024-11-29 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
        migrations.RemoveField(
            model_name='listenerprofile',
            name='telegram_id',
        ),
        migrations.RemoveField(
            model_name='listenerprofile',
            name='telegram_username',
        ),
        migrations.AddField(
            model_name='customuser',
            name='roles',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='listenerprofile',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.eventprogram'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listenerprofile',
            name='name',
            field=models.CharField(default='Eugene', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='customuser_groups', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_permissions', to='auth.permission'),
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('event_program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='events.eventprogram')),
                ('listener', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registrations', to='events.listenerprofile')),
            ],
            options={
                'unique_together': {('listener', 'event_program')},
            },
        ),
    ]
