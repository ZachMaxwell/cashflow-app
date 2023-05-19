from django.shortcuts import render
from django.db.models import Sum
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import MonthlyInputList, DataInputList, DataInputItem
from django.urls import reverse, reverse_lazy
from .forms import DataInputItemForm, DataInputListForm

import matplotlib.pyplot as plt
import pandas as pd
from .utils import get_deposit_plot, get_expense_plot, get_investment_plot

#--------PLOT VIEW------------

def plot_view(request):

    qs = DataInputItem.objects.values_list('amount', 'entry_type', 'category', 'monthly_input_list')
        
    df = pd.DataFrame(list(qs), columns=['amount', 'entry_type', 'category', 'monthly_input_list'])
    
    qs_monthlyinputlist = MonthlyInputList.objects.all()
    qs_datainputitem = DataInputItem.objects.all()

    x = [x.month for x in qs_monthlyinputlist]
    print(x)

    available_months_ids = set([x.monthly_input_list.id for x in qs_datainputitem])
    print(available_months_ids)

    y_total_expenses = []
    y_total_deposits = []
    y_total_investments = []
    for monthly_id in available_months_ids:
        y_total_expenses.append(df.loc[(df['entry_type'] == 'EXPENSE') & (df['monthly_input_list'] == monthly_id), 'amount'].sum())
        y_total_deposits.append(df.loc[(df['entry_type'] == 'DEPOSIT') & (df['monthly_input_list'] == monthly_id), 'amount'].sum())
        y_total_investments.append(df.loc[(df['entry_type'] == 'INVESTMENT') & (df['monthly_input_list'] == monthly_id), 'amount'].sum())
    print(y_total_expenses)
    print(y_total_deposits)
    print(y_total_investments)
    
    chart_expenses = get_expense_plot(x, y_total_expenses)
    chart_deposits = get_deposit_plot(x, y_total_deposits)
    chart_investments = get_investment_plot(x, y_total_investments)

    return render(request, 'finance_spreadsheet_app/plot.html', {'chart_expenses': chart_expenses, 'chart_deposits': chart_deposits, 'chart_investments': chart_investments})     


#--------MONTHLY LIST VIEWS---------

class MonthlyListView(ListView):
    model = MonthlyInputList
    template_name = "finance_spreadsheet_app/monthly_list_view.html"
    
    def get_context_data(self):
        context = super(MonthlyListView, self).get_context_data()
        print("\n")
        print("This is the monthly list view context: ")
        print(context)
        
        return context

class MonthlyListCreate(CreateView):
    model = MonthlyInputList
    fields = ['month']

    def get_context_data(self):
        context = super(MonthlyListCreate, self).get_context_data()
        print(context)
        context['month'] = "Create a new monthly entry"
        return context

class MonthlyListDelete(DeleteView):
    model = MonthlyInputList
    success_url = reverse_lazy("index")

#--------DAILY LIST VIEWS---------
class ListListView(ListView):
    model = DataInputList
    template_name = "finance_spreadsheet_app/daily_list_view.html"

    def get_queryset(self):
        print("\n")
        print("All objects in DataInputList: ")
        print(DataInputList.objects.all())
        print("\n")
        print("All objects in DataInputList with the CURRENT monthly_input_list_id: ")
        print(DataInputList.objects.filter(monthly_input_list_id=self.kwargs["monthly_list_id"]))
        print("\n")
        print("All objects in MonthlyInputList for the CURRENT monthly_input_list_id: ")
        print(MonthlyInputList.objects.get(id=self.kwargs["monthly_list_id"]))
        return DataInputList.objects.filter(monthly_input_list_id=self.kwargs["monthly_list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        print("\n")
        print("Printing ListListView context: ")
        context["monthly_input_list"] = MonthlyInputList.objects.get(id=self.kwargs["monthly_list_id"])

        # DISPLAY BALANCE SECTION -- Trying to display the balance for each list (need the list ID)
        print("\n")
        print("Printing addition of display balance context additions in the context: ")
        try:
            context['deposit_total'] = DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], entry_type='DEPOSIT').aggregate(Sum('amount')).get('amount__sum')
            context['expense_total'] = DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], entry_type='EXPENSE').aggregate(Sum('amount')).get('amount__sum')
            context['goeo_total'] = DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], category='GOEO').aggregate(Sum('amount')).get('amount__sum')
            context['car_total'] = DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], category='CAR').aggregate(Sum('amount')).get('amount__sum')
            context['rent_total'] = DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], category='RENT').aggregate(Sum('amount')).get('amount__sum')
            context['miscellaneous_total'] = DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], category='MISCELLANEOUS').aggregate(Sum('amount')).get('amount__sum')
            context['loan_total'] = DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], category='LOANS').aggregate(Sum('amount')).get('amount__sum')
            context['investment_total'] = DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], category='INVESTMENT').aggregate(Sum('amount')).get('amount__sum')
            context['subscription_total'] = DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], category='SUBSCRIPTIONS').aggregate(Sum('amount')).get('amount__sum')
            context['grocery_total'] = DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], category='GROCERY').aggregate(Sum('amount')).get('amount__sum')
            context['net_difference'] = DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], entry_type='DEPOSIT').aggregate(Sum('amount')).get('amount__sum') - DataInputItem.objects.all().filter(monthly_input_list_id=self.kwargs["monthly_list_id"], entry_type='EXPENSE').aggregate(Sum('amount')).get('amount__sum')
        
        except TypeError:
            print("Some of the database fields don't have any data yet")
        print(context)

        return context

class ListCreate(CreateView):
    model = DataInputList
    form_class = DataInputListForm

    def get_initial(self):
        initial_data = super(ListCreate, self).get_initial()
        monthly_input_list = MonthlyInputList.objects.get(id=self.kwargs["monthly_list_id"])
        initial_data["monthly_input_list"] = monthly_input_list
        return initial_data
    
    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        monthly_input_list = MonthlyInputList.objects.get(id=self.kwargs["monthly_list_id"])
        context["monthly_input_list"] = monthly_input_list
        context["month"] = "Add a new daily transaction to the list"
        print("\n")
        print("ListCreate context: ")
        print(context)
        return context
    
    def get_success_url(self):
        print("This is the monthly_input_list_id")
        print(self.object.monthly_input_list_id)
        return reverse("monthly-list", args=[self.object.monthly_input_list_id])
    
class ListUpdate(UpdateView):
    model = DataInputList
    form_class = DataInputListForm

    def get_context_data(self):
        context = super(ListUpdate, self).get_context_data()
        context["monthly_input_list"] = self.object.monthly_input_list
        context["title"] = "Edit transaction. I am at ListUpdate View"
        return context
    
    def get_success_url(self):
        return reverse("monthly-list", args=[self.object.monthly_input_list_id])

class ListDelete(DeleteView):
    model = DataInputList

    def get_success_url(self):
        return reverse_lazy("monthly-list", args=[self.kwargs["monthly_list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("printing ListDelete context before adding monthly_input_list object: ")
        print("\n")
        print(context)
        context["monthly_input_list"] = self.object.monthly_input_list
        print("\n")
        print("printing ListDelete context: ")
        print(context)
        return context

#--------ITEM VIEWS---------
class ItemListView(ListView):
    model = DataInputItem
    template_name = "finance_spreadsheet_app/daily_item_view.html"

    def get_queryset(self):
        print("\n")
        print("All deposit items in DataInputItem: ")
        print(DataInputItem.objects.filter(entry_type='DEPOSIT'))
        return DataInputItem.objects.filter(data_input_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["data_input_list"] = DataInputList.objects.get(id=self.kwargs["list_id"])
        context["monthly_input_list"] = MonthlyInputList.objects.get(id=self.kwargs["monthly_list_id"])
        return context

class ItemCreate(CreateView):
    model = DataInputItem
    form_class = DataInputItemForm

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        data_input_list = DataInputList.objects.get(id=self.kwargs["list_id"])
        monthly_input_list = MonthlyInputList.objects.get(id=self.kwargs["monthly_list_id"])
        initial_data["data_input_list"] = data_input_list
        initial_data["monthly_input_list"] = monthly_input_list
        return initial_data
    
    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        data_input_list = DataInputList.objects.get(id=self.kwargs["list_id"])
        monthly_input_list = MonthlyInputList.objects.get(id=self.kwargs["monthly_list_id"])
        context["data_input_list"] = data_input_list
        context["monthly_input_list"] = monthly_input_list
        context["title"] = "Add a new transaction to the list"
        return context
    
    def get_success_url(self):
        return reverse("item-list", args=[self.object.monthly_input_list_id, self.object.data_input_list_id])

class ItemUpdate(UpdateView):
    model = DataInputItem
    form_class = DataInputItemForm

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["monthly_input_list"] = self.object.monthly_input_list
        context["data_input_list"] = self.object.data_input_list
        context["title"] = "Edit transaction:"
        print("This is the ItemUpdate context: ")
        print(context)
        return context
    
    def get_success_url(self):
        return reverse("item-list", args=[self.object.monthly_input_list_id, self.object.data_input_list_id])

class ItemDelete(DeleteView):
    model = DataInputItem

    def get_success_url(self):
        return reverse_lazy("item-list", args=[self.object.monthly_input_list_id, self.object.data_input_list_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["monthly_input_list"] = self.object.monthly_input_list
        context["data_input_list"] = self.object.data_input_list
        print(context)
        return context

    
