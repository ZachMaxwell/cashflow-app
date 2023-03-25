from django import forms
from .models import DataInputItem, DataInputList

class DataInputItemForm(forms.ModelForm):
    class Meta:
        model = DataInputItem
        fields = [
            'amount', 
            'category', 
            'description', 
            'entry_type', 
            'entry_date', 
            'data_input_list',
            'monthly_input_list'
        ]

class DataInputListForm(forms.ModelForm):
    class Meta:
        model = DataInputList
        fields = [
            'title',
            'monthly_input_list'
        ]
