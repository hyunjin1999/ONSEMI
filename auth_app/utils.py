from django.http import HttpResponseForbidden

def family_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'FAMILY':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("페이지 접근 권한이 없습니다.")
    return _wrapped_view

def volunteer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'VOLUNTEER':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("페이지 접근 권한이 없습니다.")
    return _wrapped_view