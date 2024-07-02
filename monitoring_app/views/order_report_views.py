from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_date
from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from ..forms import FilterForm
from orders_app.models import Order, OrderItem
from shop_app.models import Category
from datetime import datetime, time
import csv

# 맥 전용 한글 폰트        
from matplotlib import rc
rc('font', family='AppleGothic')

@login_required
def generate(request):
    # 필터 폼 초기화 및 모든 카테고리 가져오기
    form = FilterForm(request.POST or None)
    categories = Category.objects.all()
    
    graph_url = None
    pie_chart_url = None

    if request.method == 'POST' and form.is_valid():
        # 폼 데이터 가져오기
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        category = form.cleaned_data.get('category')
        
        # 사용자 이메일로 주문 필터링(중복이 없을 것으로 추측)
        orders = Order.objects.filter(email=request.user.email)
        if start_date:
            start_date = make_aware(datetime.combine(start_date, time.min))
            orders = orders.filter(created__gte=start_date)
        if end_date:
            end_date = make_aware(datetime.combine(end_date, time.max))
            orders = orders.filter(created__lte=end_date)
        if category and category != 'all':
            orders = orders.filter(items__product__category=category).distinct()

        # 주문 데이터 프레임으로 변환
        data = []
        for order in orders:
            for item in order.items.all():
                data.append({
                    'Order ID': order.id,
                    'Product': item.product.name,
                    'Category': item.product.category.name,
                    'Price': float(item.price),
                    'Quantity': item.quantity,
                    'Total Cost': float(item.price * item.quantity),
                    'Created': order.created.isoformat(),
                })
        df = pd.DataFrame(data)
        df['Created'] = pd.to_datetime(df['Created'], format='ISO8601', errors='coerce')
        df['Quantity'] = df['Quantity'].astype(float)
        
        if not df.empty:
            # 꺾은선 그래프 생성
            plt.figure(figsize=(10, 6))

            if category == 'all':
                df['Date'] = df['Created'].dt.date
                daily_data = df.groupby(['Date', 'Category'])['Quantity'].sum().unstack().fillna(0)
                for column in daily_data.columns:
                    plt.plot(daily_data.index, daily_data[column], marker='o', label=column)
                plt.legend(title='카테고리')

            else:
                df['Date'] = df['Created'].dt.date
                category_name = Category.objects.get(id=category).name
                daily_data = df[df['Category'] == category_name].groupby('Date')['Quantity'].sum()
                plt.plot(daily_data.index, daily_data, marker='o')
                plt.title(f'{category_name}의 일간 주문량')
            plt.xlabel('기간')
            plt.ylabel('주문량')
            plt.xlim([start_date.date(), end_date.date()])
            plt.xticks(rotation=45)
            plt.tight_layout()

            # 그래프 이미지를 메모리에 저장
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            graph_url = base64.b64encode(image_png).decode('utf-8')
            graph_url = 'data:image/png;base64,' + graph_url

        # 전체 데이터 기반 원형 그래프 생성
        all_orders = Order.objects.filter(email=request.user.email)

        if start_date:
            all_orders = all_orders.filter(created__gte=start_date)

        if end_date:
            all_orders = all_orders.filter(created__lte=end_date)
        
        all_data = []

        for order in all_orders:
            for item in order.items.all():
                all_data.append({
                    'Category': item.product.category.name,
                    'Quantity': item.quantity,
                })

        all_df = pd.DataFrame(all_data)
        all_df['Quantity'] = all_df['Quantity'].astype(float)

        if not all_df.empty:
            plt.figure(figsize=(10, 6))
            category_counts = all_df.groupby('Category')['Quantity'].sum()
            plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')

            # 원형 그래프 이미지를 메모리에 저장
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            pie_chart_url = base64.b64encode(image_png).decode('utf-8')
            pie_chart_url = 'data:image/png;base64,' + pie_chart_url

        for record in data:
            record['Price'] = float(record['Price'])
            record['Total Cost'] = float(record['Total Cost'])

        request.session['filtered_orders'] = data

    return render(request, 'monitoring_app/generate.html', {'form': form, 'categories': categories, 'graph_url': graph_url, 'pie_chart_url': pie_chart_url})

@login_required
def csv_view(request):

    # 필터된 주문 데이터를 세션에서 가져와 csv_view 템플릿으로 전달
    filtered_orders = request.session.get('filtered_orders', [])
    return render(request, 'monitoring_app/csv_view.html', {'filtered_orders': filtered_orders})

@login_required
def download_csv(request):

    # 필터 데이터를 기반으로 주문 데이터 다운로드
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_id = request.GET.get('category')
    
    orders = Order.objects.filter(email=request.user.email, paid=True)
    if start_date:
        start_date = make_aware(datetime.combine(parse_date(start_date), time.min))
        orders = orders.filter(created__gte=start_date)

    if end_date:
        end_date = make_aware(datetime.combine(parse_date(end_date), time.max))
        orders = orders.filter(created__lte=end_date)

    if category_id and category_id != 'all':
        orders = orders.filter(items__product__category__id=category_id).distinct()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Product', 'Price', 'Quantity', 'Total Cost', 'Created'])

    for order in orders:
        for item in order.items.all():
            writer.writerow([order.id, item.product.name, item.price, item.quantity, item.get_cost(), order.created])

    return response