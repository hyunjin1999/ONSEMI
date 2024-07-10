from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import transaction
from auth_app.models import User
from management_app.models import Care, Senior
from auth_app.utils import family_required  # 해당 페이지는 보호자로 로그인했을 때만 접근이 가능하게 수정!!


# Create your views here.

# 1 -> easy
# user(보호자)가 노인을 등록하는 기능 (예상 : html파일 1+개?)
#       -> 위에거 수정하는 페이지(html1개+)


# 2 -> normal
# user(보호자)가 Care를 등록하는 기능(예상 :html파일 1+개?) -> 어려움
#       -> 위에거 수정하는 페이지(html1개+)

# 3 ->개어렵
# user(봉사자)가 user(보호자)가 올린 Care를 확인하는 = 조회하는 기능(예상 :html 1+개?)
# 여러 방면으로 조회할 수 있어야함 ( 노인 카테고리로 조회, 오름차순, 내림차순, or 유저별로, 지역별로, 날짜별로 오름차순)
# NOT_APPROVED, CONFIRMED, APPROVED
# 4 ->hard
# user(보호자)가 자신이 올린 Care를 확인하는 기능(예상: html 1개 이상)
# 여러 방면으로 조회할 수 있어야함
# 위에거랑 같은데 유저별은 없겠죠?
# NOT_APPROVED, CONFIRMED, APPROVED


@login_required
@family_required
def add_care(request):
    if request.method == "GET":
        user = request.user
        user = User.objects.get(pk=user.id)
        user_senior_list = user.senior_set.all()
        context = {"seniors": user_senior_list}
        return render(request, "management_app/add_care.html", context)

    if request.method == "POST":
        care_type = request.POST.get("care_type")
        title = request.POST.get("title")
        content = request.POST.get("content")
        senior = request.POST.get("senior")
        parkinson_diagnosis = request.POST.get("parkinson_diagnosis")
        
        if parkinson_diagnosis == "on":
            parkinson_diagnosis = True
        else:
            parkinson_diagnosis = False
                
        user = request.user
        user = get_object_or_404(User, pk=user.id)

        care = Care(
            care_type=care_type,
            title=title,
            content=content,
            user_id=user,
            parkinson_diagnosis = parkinson_diagnosis,
        )
        care.save()

        user_senior = Senior.objects.get(pk=senior)
        care.seniors.add(user_senior)

        return redirect("/monitoring/family_monitor/")


@login_required
@family_required
def show_one_care(request, care_id):
    care = Care.objects.get(pk=int(care_id))
    if request.method == 'POST':
        care_state = request.POST.get('care_state')
        admin_message = request.POST.get('admin_message')

        if care_state in ['APPROVED', 'REJECT']:
            care.care_state = care_state
        care.admin_message = admin_message
        care.save()
        return redirect('show_one_care', care_id=care_id)

    context = {"care": care}
    return render(request, "management_app/show_one_care.html", context)


@login_required
@family_required
def update_care(request, care_id):
    care = get_object_or_404(Care, pk=care_id)

    if request.method == "GET":
        seniors = Senior.objects.filter(user_id=care.user_id)
        context = {"care": care, "seniors": seniors}
        return render(request, "management_app/update_one_care.html", context)

    elif request.method == "POST":
        care_type = request.POST.get("care_type")
        title = request.POST.get("title")
        content = request.POST.get("content")
        senior_id = request.POST.get("senior")
        parkinson_diagnosis = request.POST.get("parkinson_diagnosis")

        if care_type:
            care.care_type = care_type
        if title:
            care.title = title
        if content:
            care.content = content
        if senior_id:
            selected_senior = Senior.objects.get(pk=int(senior_id))
            care.seniors.clear()  # Clear existing seniors
            care.seniors.add(selected_senior)  # Add the selected senior
            
        if parkinson_diagnosis == "on":
            care.parkinson_diagnosis = True
        else:
            care.parkinson_diagnosis = False

        care.save()
        return redirect(f"/management/care/detail/{care_id}/")

@login_required
@family_required
def delete_care(request, care_id):
    care = get_object_or_404(Care, id=care_id)
    care.delete()
    return redirect('/monitoring/family_monitor/') 

  
@login_required
@family_required
def add_senior(request):
    if request.method == "GET":
        context = {"ages": [i for i in range(1, 120)]}
        return render(request, "management_app/add_senior.html", context)

    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        has_alzheimers = request.POST.get("has_alzheimers")
        has_parkinsons = request.POST.get("has_parkinsons")
        photo = request.FILES.get("photo")
        user = request.user

        # user = User.objects.get(pk=user.id)

        # 기존에 재홍님께서 작성한 코드로는 이상하게 오류가 발생해서 새롬게 작성
        user = request.user
        senior = Senior(
            name=name,
            address=address,
            age=age,
            gender=gender,
            phone_number=phone_number,
            has_alzheimers =has_alzheimers,
            has_parkinsons = has_parkinsons,
            user_id=user,
            photo = photo,
        )

        senior.save()

        return redirect("/management/senior/list/")


@login_required
@family_required
def update_senior(request, id):
    senior = get_object_or_404(Senior, id=id)
    
    if request.method == 'POST':
        senior.name = request.POST.get('name', senior.name)
        senior.age = request.POST.get('age', senior.age)
        senior.gender = request.POST.get('gender', senior.gender)
        senior.phone_number = request.POST.get('phone', senior.phone_number)
        senior.has_alzheimers = request.POST.get('has_alzheimers') 
        senior.has_parkinsons = request.POST.get('has_parkinsons')

        if 'photo' in request.FILES:
            senior.photo = request.FILES['photo']
        
        senior.save()
        return redirect('/management/senior/list/')
    
    context = {
        'senior': senior,
    }
    return render(request, 'management_app/update_senior.html', context)


@login_required
@family_required
def delete_senior(request, id):
    # 노인 객체 가져오기
    senior = get_object_or_404(Senior, id=id)

    if request.method == 'POST':
        #    pass

        # 노인 삭제
        senior.delete()

        # 삭제 후 리디렉션할 URL 설정 (선택 사항)
        return redirect('/management/senior/list/')  # 사용자의 노인 리스트 화면으로 리디렉션
    # return render(request, 'management_app/senior_confirm_delete.html', {'senior': senior})