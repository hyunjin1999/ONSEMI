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

def terms(request):
    return render(request,'page/terms.html')

def user_page(request):
    user_type = request.user.user_type
    if user_type == 'FAMILY':
        return render(request, 'page/family.html')
    elif user_type == 'VOLUNTEER':
        return render(request, 'page/volunteer.html')
    elif user_type == 'ADMIN':
        return render(request, 'admin_dashboard')
    return render(request, 'default_dashboard') 