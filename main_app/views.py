from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'page/index.html')

def introduce(request):
    return render(request, 'page/introduce.html')

def family(request):
    return render(request, 'page/family.html')

def volunteer(request):
    return render(request,'page/volunteer.html')

def monitor(request):
    return render(request,'page/monitor.html')