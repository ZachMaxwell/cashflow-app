# Generated by Django 4.1.5 on 2023-03-01 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance_spreadsheet_app', '0004_alter_datainputitem_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyInputList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=15, null=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='datainputlist',
            name='monthly_input_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='finance_spreadsheet_app.monthlyinputlist'),
        ),
    ]
