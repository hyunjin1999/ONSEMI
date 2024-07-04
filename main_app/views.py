from django.shortcuts import render
from management_app.models import Senior, Care
from django.contrib.auth.decorators import login_required
from auth_app.models import User

#Create your views here.
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

@login_required
def user_page(request):
    user_type = request.user.user_type
    
    if user_type == 'FAMILY':
        user_id = request.user.id
        seniors = Senior.objects.filter(user_id=user_id)
        context = {
            'seniors': seniors
        }
        return render(request, 'management_app/user_senior_list.html', context)
     
    elif user_type == 'VOLUNTEER':
        sort_by = request.GET.get("sort_by", "datetime")
        order = request.GET.get("order", "asc")
        user_id = request.GET.get("user", "")

        if order == "desc":
            sort_by = "-" + sort_by

        cares = Care.objects.all()

        if user_id:
            cares = cares.filter(user_id=user_id)

        cares = cares.order_by(sort_by)
        users = User.objects.all()

        context = {
            "cares": cares,
            "users": users,
            "selected_user": user_id,
        }

        return render(request, "management_app/volunteer_care_list.html", context)        
    
    elif user_type == 'ADMIN':
        return render(request, 'admin_dashboard')
    
    return render(request, 'default_dashboard') 

