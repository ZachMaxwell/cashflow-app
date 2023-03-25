from django.utils import timezone
from django.db import models
from django.urls import reverse
from django import forms


class MonthlyInputList(models.Model):
    month = models.CharField(max_length = 15, unique = True, null=True)

    def get_absolute_url(self):
        return reverse("monthly-list", args=[self.id])

    def __str__(self): 
        return self.month

class DataInputList(models.Model):
    title = models.CharField(max_length = 15, unique = True, null=True)
    monthly_input_list = models.ForeignKey(MonthlyInputList, on_delete = models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse(
                "list-update", args=[str(self.monthly_input_list.id), str(self.id)]
                )

    def __str__(self): 
        return self.title
    
    class Meta:
        ordering = ["title"]

class DataInputItem(models.Model):

    ENTRY_TYPE_CHOICES = [
        ('DEPOSIT', 'Deposit'),
        ('EXPENSE', 'Expense'),

    ]
   
    CATEGORY_CHOICES = [
        ('GOEO', 'Going out & Eating out'),
        ('CAR', 'Car, Gas, & Auto Insurance'),
        ('RENT', 'Rent & Utilities'),
        ('MISCELLANEOUS', 'Personal, Travel, & other Events'),
        ('LOANS', 'Loan Payments'),
        ('INVESTMENTS', 'Investment Contributions' ),
        ('SUBSCRIPTIONS', 'Subscriptions' ),
        ('GROCERY', 'Grocery'),
        ('DEPOSIT', 'Deposit'),

    ]
    
    amount = models.DecimalField(max_digits = 12, decimal_places = 2, null = True)
    description = models.TextField(null=True, blank=True)
    entry_type = models.CharField(max_length = 100, choices = ENTRY_TYPE_CHOICES, default = 'EXPENSE', null=True)
    entry_date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length = 100, choices = CATEGORY_CHOICES, default = 'MISCELLANEOUS', null=True)
    data_input_list = models.ForeignKey(DataInputList, on_delete = models.CASCADE, null=True)
    monthly_input_list = models.ForeignKey(MonthlyInputList, on_delete = models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse(
                "item-update", args=[str(self.monthly_input_list), str(self.data_input_list.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.description}: {self.amount}"

    class Meta:
        ordering = ["entry_date"]
