from celery import shared_task
import pandas as pd
from shop_app.models import Product
from django.shortcuts import get_object_or_404


@shared_task(bind=True)
def add(self, x, y):
    print(f"Task {self.request.id} started with arguments: {x}, {y}")
    result = x + y
    print(f"Task {self.request.id} finished with result: {result}")
    return result


@shared_task(bind=True)
def update_product_price(self):

     # 가장 최근 상품 가격 불러오기
    data = pd.read_csv('./total.csv')
    data = data.iloc[-1] 
    
    for item, value in data.iloc[1:].items():
        product = get_object_or_404(Product, name=item)
        print(product)
        product.price = value
        product.save()
    