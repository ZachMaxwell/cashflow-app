# Generated by Django 4.1.5 on 2023-03-11 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance_spreadsheet_app', '0005_monthlyinputlist_datainputlist_monthly_input_list'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datainputlist',
            options={'ordering': ['title']},
        ),
    ]
