from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'page/index.html')

def introduce(request):
    return render(request, 'page/introduce.html')

def family(request):
    return render(request, 'page/family.html')

def mypage(request):
    return render(request, 'page/mypage.html')

def order(request):
    return render(request, 'page/order.html')