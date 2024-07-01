from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import transaction
from auth_app.models import User
from care_app.models import Care, Senior

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


# @login_required
def add_care(request):
    if request.method == "GET":
        user = request.user
        user = User.objects.get(pk=user.id)
        user_senior_list = user.senior_set.all()
        context = {"seniors": user_senior_list}
        return render(request, "care_app/add_care.html", context)

    if request.method == "POST":
        care_type = request.POST.get("care_type")
        title = request.POST.get("title")
        content = request.POST.get("content")
        senior = request.POST.get("senior")

        user = request.user
        user = get_object_or_404(User, pk=user.id)

        care = Care(
            care_type=care_type,
            title=title,
            content=content,
            user_id=user,
        )
        care.save()

        user_senior = Senior.objects.get(pk=senior)
        care.seniors.add(user_senior)

        return redirect("/care/my-cares/")


def show_one_care(request, care_id):
    care = Care.objects.get(pk=int(care_id))
    username = care.user_id.username
    context = {"care": care}

    return render(request, "care_app/show_one_care.html", context)


# @login_required
def update_care(request, care_id):
    if request.method == "GET":
        care = Care.objects.get(pk=int(care_id))
        seniors = care.seniors.all()
        context = {"care": care, "seniors": seniors}
        return render(request, "care_app/update_one_care.html", context)

    if request.method == "POST":

        care_type = request.POST.get("care_type")
        title = request.POST.get("title")
        content = request.POST.get("content")

        care = Care.objects.get(pk=int(care_id))

        if care_type:
            care.care_type = care_type
        if title:
            care.title = title
        if content:
            care.content = content
        care.save()
        return redirect(f"/care/care/detail/{care_id}/")

def delete_care(request, care_id):
    care = get_object_or_404(Care, id=care_id)
    care.delete()

    return redirect('/care/my-cares/') 


# @login_required
def add_senior(request):
    if request.method == "GET":
        context = {"ages": [i for i in range(1, 120)]}
        return render(request, "care_app/add_senior.html", context)

    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        has_alzheimers = request.POST.get("has_alzheimers")
        has_parkinsons = request.POST.get("has_parkinsons")
        user = request.user

        user = User.objects.get(pk=user.id)
        senior = Senior(
            name=name,
            address=address,
            age=age,
            gender=gender,
            phone_number=phone_number,
            user_id=user,
        )
        if has_parkinsons:
            senior.has_parkinsons = True
        if has_alzheimers:
            senior.has_alzheimers = True

        senior.save()

        return redirect("/care/senior/list/")


# @login_required  
def update_senior(request, id):
    senior = get_object_or_404(Senior, id=id)
    
    if request.method == 'POST':
        senior.name = request.POST.get('name')
        senior.age = request.POST.get('age')
        senior.gender = request.POST.get('gender')
        senior.phone_number = request.POST.get('phone')
        senior.has_alzheimers = 'has_alzheimers' in request.POST
        senior.has_parkinsons = 'has_parkinsons' in request.POST



        senior.save()
        return redirect('/care/senior/list/')

    context = {
        'senior': senior
    }
    return render(request, 'care_app/update_senior.html', context)

def delete_senior(request, id):
    # 노인 객체 가져오기
    senior = get_object_or_404(Senior, id=id)

    #if senior.user_id != request.user.id:
    #    pass

    # 노인 삭제
    senior.delete()

    # 삭제 후 리디렉션할 URL 설정 (선택 사항)
    return redirect('/care/senior/list/')  # 사용자의 노인 리스트 화면으로 리디렉션