# Generated by Django 5.0.1 on 2024-01-26 07:14

import django.db.models.deletion
import tickets.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('associates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('assigned', 'Assigned'), ('work_in_progress', 'Work in Progress'), ('processed', 'Processed'), ('completed', 'Completed'), ('returned', 'Returned')], max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('type', models.IntegerField(choices=[(1, 'Type 1'), (2, 'Type 2'), (3, 'Type 3')])),
                ('description', models.TextField(default='Describe your task here.')),
                ('uploaded_file', models.FileField(blank=True, null=True, upload_to=tickets.models.ticket_upload_files)),
                ('uploaded_image', models.ImageField(blank=True, null=True, upload_to=tickets.models.ticket_upload_files)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('associate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='associates', to='associates.associate')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='tickets.category')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='associates.userdepartment')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='FollowUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=tickets.models.upload_follow_ups)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followups', to='tickets.ticket')),
            ],
            options={
                'verbose_name': 'FollowUp',
                'verbose_name_plural': 'FollowUps',
                'ordering': ('-created_date',),
            },
        ),
    ]
