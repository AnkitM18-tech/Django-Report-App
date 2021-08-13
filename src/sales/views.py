from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from .utils import get_salesman_from_id,get_customer_from_id,get_chart

from django.contrib.auth.decorators import login_required   #for function based views use this decorator
from django.contrib.auth.mixins import LoginRequiredMixin   #For class based views the first argument

# Create your views here.
@login_required
def home_view(request):
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    no_data = None

    if request.method == "POST":
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
        # print(date_from, date_to, chart_type)
        
        sale_qs = Sale.objects.filter(created__date__lte= date_to, created__date__gte = date_from)
        if len(sale_qs) > 0:
            sales_df = pd.DataFrame(sale_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x:x.strftime('%Y-%m-%d'))
            sales_df.rename({"customer_id":"customer" , "salesman_id":"salesman" , "id":"sales_id"}, axis=1,inplace=True)
            position_data = []

            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id':pos.id,
                        'product':pos.product.name,
                        'quantity':pos.quantity,
                        'price':pos.price,
                        'sales_id':pos.get_sales_id(),
                    }
                    position_data.append(obj)

            positions_df = pd.DataFrame(position_data)
            merged_df = pd.merge(sales_df,positions_df, on="sales_id")

            df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')

            chart = get_chart(chart_type, sales_df, results_by)

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html() 
            df = df.to_html()
        else:
            no_data = "No Data is Available in this Date Range !"


    context ={
        'search_form':search_form,
        'report_form':report_form,
        'sales_df':sales_df,
        'positions_df':positions_df,
        'merged_df':merged_df,
        'df':df,
        'chart':chart,
        'no_data':no_data,
    }
    return render(request, 'sales/home.html', context)

class SalesListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/main.html'

class SalesDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/detail.html'        #if we won't set template_name it will be default model_detail.html in this case sale_detail.html

@login_required
def sale_list_view(request):
    qs = Sale.objects.all()
    return render(request, 'sales/main.html', {'object_list':qs})

@login_required
def detail_view_list(request,pk):
    obj = Sale.objects.get(pk=pk)      #pk = kwargs.get('pk')
    #or
    #obj = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/detail.html', {'object':obj})

    """
    in the urls :
    path('sales/', sale_list_view, name='list'),
    path('sales/<pk>/', sale_detail_view, name = 'detail'),
    """