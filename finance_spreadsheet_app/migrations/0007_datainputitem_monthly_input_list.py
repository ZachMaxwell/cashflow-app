# Generated by Django 4.1.5 on 2023-03-17 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance_spreadsheet_app', '0006_alter_datainputlist_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='datainputitem',
            name='monthly_input_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='finance_spreadsheet_app.monthlyinputlist'),
        ),
    ]
