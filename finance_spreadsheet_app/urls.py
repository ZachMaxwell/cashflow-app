from django.urls import path
from . import views

"""
urlpatterns looks at incoming HTTP requests and matches the pattern of the url being requested 
with the appropriate view.
"""
urlpatterns = [
    
    #MONTHLY LIST
    path("", views.MonthlyListView.as_view(), name="index"),
    path("monthly_list/<int:monthly_list_id>/", views.ListListView.as_view(), name='monthly-list'),

    path("monthly_list/add/", views.MonthlyListCreate.as_view(), name="monthly-list-add"),
    path("monthly_list/<int:monthly_list_id>/delete/", views.MonthlyListDelete.as_view(), name="monthly-list-delete"),

    #DAILY LIST
    #TODO - change the name of index to something else
    path("monthly_list/<int:monthly_list_id>/list/", views.ListListView.as_view(), name="list"),
    path("monthly_list/<int:monthly_list_id>/list/add/", views.ListCreate.as_view(), name="list-add"),
    path("monthly_list/<int:monthly_list_id>/list/<int:pk>/",  views.ListUpdate.as_view(), name = "list-update"),
    path("monthly_list/<int:monthly_list_id>/list/<int:pk>/delete/", views.ListDelete.as_view(), name="list-delete"),

    #DAILY ITEMS
    path("monthly_list/<int:monthly_list_id>/list/<int:list_id>/item", views.ItemListView.as_view(), name="item-list"),
    path("monthly_list/<int:monthly_list_id>/list/<int:list_id>/item/add", views.ItemCreate.as_view(), name="item-add"),
    path("monthly_list/<int:monthly_list_id>/list/<int:list_id>/item/<int:pk>/", views.ItemUpdate.as_view(), name="item-update"),
    path("monthly_list/<int:monthly_list_id>/list/<int:list_id>/item/<int:pk>/delete/", views.ItemDelete.as_view(), name="item-delete"),


    ]

