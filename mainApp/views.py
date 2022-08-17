from django.http import HttpResponseRedirect
from django.shortcuts import render


def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_email = request.COOKIES.get('username')
            c_uid = request.COOKIES.get("uid")
            if not c_email or not c_uid:
                return HttpResponseRedirect('/index/login')
            else:
                # 回写session
                request.session['username'] = c_email
                request.session['uid'] = c_uid
        return fn(request, *args, **kwargs)

    return wrap


# Create your views here.
@check_login
def index(request):
    if request.method == "GET":
        username = request.session.get("username")
        return render(request, "mainApp/index.html", locals())


def blog(request):
    return render(request, "my_blog_index/my_blog_index.html")
