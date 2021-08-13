from django.urls import path
from .views import (
    home_view, SalesListView,SalesDetailView
)

app_name = 'sales'

urlpatterns = [
    path('', home_view,name= 'home'),
    path('sales/', SalesListView.as_view(),name= 'list'),            #.as_view() for class based view
    path('sales/<pk>/', SalesDetailView.as_view(),name = 'detail')         #pk will decide which object to display
]