from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from django.http import HttpResponse

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64
import csv 

from ..forms import FilterForm
from orders_app.models import Order
from datetime import datetime, time
from management_app.models import Care , Senior

@login_required
def download_order_csv(request):
    filtered_orders = request.session.get('filtered_orders', [])
    
    # 데이터프레임으로 변환
    df = pd.DataFrame(filtered_orders)

    # 'Created' 컬럼이 있는 경우 'created'로 이름 변경
    if 'Created' in df.columns:
        df.rename(columns={'Created': 'created'}, inplace=True)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="filtered_orders.csv"'
    response.write(u'\ufeff'.encode('utf8'))  # UTF-8 BOM 추가, 아니면 한글이 깨짐

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Product', 'Category', 'Price', 'Quantity', 'Total Cost', 'Created'])

    for order in df.to_dict('records'):
        writer.writerow([
            order['Order_ID'], 
            order['Product'], 
            order['Category'], 
            order['Price'], 
            order['Quantity'], 
            order['Total_Cost'], 
            order['created']
        ])

    return response

####################################################################################
@login_required
def download_care_csv(request):
    filtered_cares = request.session.get('filtered_cares', [])

    if not filtered_cares:
        return HttpResponse("데이터가 없습니다", content_type='text/plain; charset=utf-8')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="filtered_cares.csv"'
    response.write(u'\ufeff'.encode('utf8'))  # UTF-8 BOM 추가

    writer = csv.writer(response)
    writer.writerow(['Care Type', 'Datetime', 'Care State'])

    for care in filtered_cares:
        writer.writerow([care['care_type'], care['datetime'], care['care_state']])

    return response