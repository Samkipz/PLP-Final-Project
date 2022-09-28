from django.http import HttpResponse
# from functools import wraps
from django.core.exceptions import PermissionDenied

# def ajax_login_required(view):
#     @wraps(view)
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_authenticated():
#             raise PermissionDenied
#         return view(request, *args, **kwargs)
#     return wrapper


def ajax_login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
            # url = request.META.get('HTTP_REFERER', '/')
            # resp_body = '<script>alert("You cannot apply for a bursary unless your account has been approved");\
            #  window.location="%s"</script>' % url
            # return HttpResponse(resp_body)
            
    return wrapper_func