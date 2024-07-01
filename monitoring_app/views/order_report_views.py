import csv
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from io import StringIO
import pandas as pd
from orders_app.models import Order, OrderItem
from ..forms import FilterForm

@login_required
def generate(request):
    form = FilterForm()
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            category = form.cleaned_data['category']

            orders = Order.objects.filter(email=request.user.email, paid=True)
            if start_date:
                orders = orders.filter(created__gte=start_date)
            if end_date:
                orders = orders.filter(created__lte=end_date)
            if category:
                orders = orders.filter(items__product__category=category).distinct()

            data = []
            for order in orders:
                for item in order.items.all():
                    data.append({
                        'Order ID': order.id,
                        'Product': item.product.name,
                        'Price': item.price,
                        'Quantity': item.quantity,
                        'Total Cost': item.get_cost(),
                        'Created': order.created,
                    })

            # DataFrame으로 변환
            df = pd.DataFrame(data)
            
            # 그래프 생성
            fig, ax = plt.subplots(2, 1, figsize=(10, 8))
            
            # 카테고리 별 상품 수
            category_data = df['Product'].value_counts()
            category_data.plot(kind='pie', autopct='%1.1f%%', ax=ax[0])
            ax[0].set_title('Product Categories')
            
            # 월별 상품 수 그래프
            df['Created'] = pd.to_datetime(df['Created'])
            monthly_data = df.groupby(df['Created'].dt.to_period('M'))['Quantity'].sum()
            monthly_data.plot(kind='line', ax=ax[1])
            ax[1].set_title('Monthly Product Sales')
            
            # 그래프 저장
            fig.savefig('monitoring_app/static/monitoring_app/report.png')
            
            return render(request, 'monitoring_app/report.html', {'form': form, 'data': data})
    return render(request, 'monitoring_app/generate.html', {'form': form})

@login_required
def download_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_id = request.GET.get('category')
    
    orders = Order.objects.filter(email=request.user.email, paid=True)
    if start_date:
        orders = orders.filter(created__gte=start_date)
    if end_date:
        orders = orders.filter(created__lte=end_date)
    if category_id:
        orders = orders.filter(items__product__category__id=category_id).distinct()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Product', 'Price', 'Quantity', 'Total Cost', 'Created'])

    for order in orders:
        for item in order.items.all():
            writer.writerow([order.id, item.product.name, item.price, item.quantity, item.get_cost(), order.created])

    return response