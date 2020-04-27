# Generated by Django 3.0.3 on 2020-04-27 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mg_manager', '0002_auto_20200426_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField()),
                ('invite_reason', models.CharField(max_length=64)),
                ('role', models.CharField(choices=[('ADMIN', 'ADMIN'), ('PARTICIPANT', 'PARTICIPANT'), ('DOCTOR', 'DOCTOR'), ('SCIENTIST', 'SCIENTIST'), ('GUEST', 'GUEST')], default='GUEST', max_length=11)),
                ('study', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mg_manager.Study')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='study',
            name='users',
            field=models.ManyToManyField(through='mg_manager.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]