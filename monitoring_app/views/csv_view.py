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
from django.utils import timezone

# 맥 전용 한글 폰트
from matplotlib import rc
rc('font', family='AppleGothic')

@login_required
def csv_view(request):
    data_type = request.GET.get('type')
    
    initial_data = {
        'start_date': request.session.get('start_date'),
        'end_date': request.session.get('end_date'),
        'category_order': request.session.get('category_order'),
        'category_service': request.session.get('category_service'),
        'selected_senior': request.session.get('selected_senior'),
    }

    form = FilterForm(request.POST or None, initial=initial_data, user=request.user)

    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        category_order = form.cleaned_data.get('category_order')
        category_service = form.cleaned_data.get('category_service')
        selected_senior = form.cleaned_data.get('selected_senior')

        request.session['start_date'] = start_date.isoformat() if start_date else None
        request.session['end_date'] = end_date.isoformat() if end_date else None
        request.session['category_order'] = category_order
        request.session['category_service'] = category_service
        request.session['selected_senior'] = selected_senior
    else:
        start_date = initial_data.get('start_date')
        end_date = initial_data.get('end_date')
        category_order = initial_data.get('category_order')
        category_service = initial_data.get('category_service')
        selected_senior = initial_data.get('selected_senior')

    if start_date and isinstance(start_date, str):
        start_date = make_aware(datetime.combine(datetime.strptime(start_date, '%Y-%m-%d'), time.min))
    if end_date and isinstance(end_date, str):
        end_date = make_aware(datetime.combine(datetime.strptime(end_date, '%Y-%m-%d'), time.max))

    if data_type == 'care':
        data_care = []
        cares = Care.objects.filter(user_id=request.user)
        if start_date:
            start_date = make_aware(datetime.combine(start_date, time.min))
            cares = cares.filter(datetime__gte=start_date)
        if end_date:
            end_date = make_aware(datetime.combine(end_date, time.max))
            cares = cares.filter(datetime__lte=end_date)
        if category_service and category_service != 'all':
            cares = cares.filter(care_type=category_service)
        if selected_senior and selected_senior != 'all':
            cares = cares.filter(seniors__id=selected_senior)

        total_cares = cares.count()
        completed_cares = cares.filter(care_state='COMPLETED').count()

        completed_rate = 0
        if total_cares > 0:
            completed_rate = (completed_cares / total_cares) * 100

        for care in cares:
            data_care.append({
                'care_type': care.care_type,
                'datetime': care.datetime.isoformat(),
                'care_state': care.care_state,
            })
        request.session['filtered_cares'] = data_care

        return render(request, 'monitoring_app/csv_view.html', {
            'filtered_cares': data_care, 
            'data_type': 'care',
            'completed_rate': completed_rate,
            'form': form,
        })
#############################################################################################
    else:
        orders = Order.objects.filter(user=request.user)
        if start_date:
            start_date = make_aware(datetime.combine(start_date, time.min))
            orders = orders.filter(created__gte=start_date)
        if end_date:
            end_date = make_aware(datetime.combine(end_date, time.max))
            orders = orders.filter(created__lte=end_date)
        if category_order and category_order != 'all':
            orders = orders.filter(items__product__category__name=category_order).distinct()
        if selected_senior and selected_senior != 'all':
            orders = orders.filter(senior_id=selected_senior)

        data = []
        for order in orders:
            for item in order.items.all():
                local_created = timezone.localtime(order.created)
                formatted_created = local_created.strftime('%Y년 %m월 %d일 %p %I:%M')
                formatted_created = formatted_created.replace('AM', '오전').replace('PM', '오후')
                data.append({
                    'order_id': order.id,
                    'product': item.product.name,
                    'category': item.product.category.name,
                    'price': float(item.price),
                    'quantity': item.quantity,
                    'total_cost': float(item.price * item.quantity),
                    'created': formatted_created,
                })


        if category_order and category_order != 'all':
            data = [order for order in data if order['Category'] == category_order]

        return render(request, 'monitoring_app/csv_view.html', {
            'filtered_orders': data, 
            'data_type': 'order',
            'form': form,
        })