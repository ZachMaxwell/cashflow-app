# Generated by Django 4.1.5 on 2023-02-11 13:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finance_spreadsheet_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datainputitem',
            name='category',
            field=models.CharField(choices=[('GOEO', 'Going out & Eating out'), ('CAR', 'Car, Gas, & Auto Insurance'), ('RENT', 'Rent & Utilities'), ('MISCELLANEOUS', 'Personal, Travel, & other Events'), ('LOANS', 'Loan Payments'), ('INVESTMENTS', 'Investment Contributions'), ('SUBSCRIPTIONS', 'Subscriptions'), ('GROCERY', 'Grocery')], default='MISCELLANEOUS', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='datainputitem',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='datainputitem',
            name='data_input_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='finance_spreadsheet_app.datainputlist'),
        ),
        migrations.AlterField(
            model_name='datainputitem',
            name='entry_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='datainputitem',
            name='entry_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datainputlist',
            name='title',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
    ]
