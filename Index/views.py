import hashlib
import time
from random import Random

from django.core import signing
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from DJyue import settings

# 生成验证码
from Index.models import NewUser


def random_str(randomlength=8):
    check_code = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        check_code += chars[random.randint(0, length)]
    return check_code


# 发送验证码
def send_check_code(request):
    email = request.GET.get("email")
    if str(email) in request.session.keys():  # 验证码已发送
        data = {
            "code": 300
        }
        return JsonResponse(data)
    email_code = random_str()
    msg = '验证码：' + email_code
    try:  # 发送成功
        send_mail('邮箱验证', msg, settings.EMAIL_FROM, [email])
        request.session[str(email)] = email_code
        request.session.set_expiry(10 * 60)
        data = {
            "code": 200
        }
        return JsonResponse(data)
    except Exception as e:  # 发送失败
        print(e)
        data = {
            "code": 400
        }
        return JsonResponse(data)


# 主页 登录
def index(request):
    if request.method == "GET":
        # 首先先判断session是否存在：
        msg = 200  # 用户已登录
        if request.session.get("username") and request.session.get("uid"):
            # 如果在就判断用户登录
            return HttpResponseRedirect("/mainindex/index", locals())
        # 获取用户的cookies
        c_username = request.COOKIES.get("username")
        c_uid = request.COOKIES.get("uid")

        # 如果cookies不存在就进行回写
        if c_username and c_uid:
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return HttpResponseRedirect("/mainindex/index", locals())
        return render(request, "index/index.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        # 将得到的密码进行哈希加密
        m = hashlib.md5()
        m.update(password.encode())
        password = m.hexdigest()
        # 从数据库中拿出用户的数据
        tips = 200  # 用户名或者密码错误
        is_active = 0
        try:
            user = NewUser.objects.get(username=username)
        except Exception as e:
            print(e)
            return render(request, "index/index.html", locals())
            # return JsonResponse({"code": 400})  # 数据库发生错误 1.不存在该用户 2.数据库出现错误
        # 判断用户是否通过管理员的同意激活
        if password != user.password:

            return render(request, "index/index.html", locals())
        else:

            if user.is_active == str(0):
                tip = 100
                tips = 300
                return render(request, "index/index.html", locals())
                # return JsonResponse({"code": 300})  # 密码错误
        request.session['username'] = user.username
        request.session['uid'] = user.id

        # 判断用户是否点击了记住账户
        # 如果用户点击了，就对cookies进行存在
        resp = HttpResponseRedirect('/mainindex/index')
        if 'number' in request.POST:
            resp.set_cookie('email', user.username, max_age=3600 * 24 * 3)
            resp.set_cookie('uid', user.id, max_age=3600 * 24 * 3)
        return resp


# 注册页面

def register(request):
    if request.method == "GET":
        return render(request, "register/register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        check_code = request.POST.get("check-code")

        # 对密码进行哈希加密
        m = hashlib.md5()
        m.update(password.encode())
        password = m.hexdigest()
        # 判断验证码是否正确
        if check_code != request.session[email]:
            code = 300
            return render(request, "register/register.html", locals())
            # return JsonResponse({"code": 300})  # 验证码错误
        # 将数据存储到数据库当中
        try:
            NewUser.objects.create(username=username, password=password, email=email)
        except Exception as e:
            print(e)
            code = 400
            return render(request, "register/register.html", locals())
            # return JsonResponse({"code": 400})  # 数据库发生未知错误，请重新尝试
        code = 200
        return render(request, "register/register.html", locals())
        # return JsonResponse({"code": 200})  # 注册成功


# 安全协议
def surprise(request):
    return render(request, "surprise/surprise.html")


# 判断用户是否存在
def is_user(request):
    username = request.GET.get("username")
    try:
        NewUser.objects.get(username=username)
    except Exception as e:
        return JsonResponse({"code": 300})  # 用户不存在
    return JsonResponse({"code": 200})  # 用户存在


# 退出登录
def logout(request):
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    resp = HttpResponseRedirect('/index/login')
    if 'username' in request.COOKIES:
        resp.delete_cookie("username")
    if 'uid' in request.COOKIES:
        resp.delete_cookie("uid")
    return resp


# 发送激活邮件
def send_email(request):
    email = request.GET.get("email")
    token = signing.dumps({"email": email, 'time': time.time()})
    verify_url = request.get_host() + "/index/re_email?token=" + str(token)
    print(verify_url)
    subject = '用户激活'
    html_message = '<p>管理员你好</p>' \
                   '<p>你有一条激活申请</p>' \
                   '<p>激活人的邮箱为：%s。请复制此链接到浏览器中打开激活账号</p>' \
                   '<p><a href="%s">%s</a></p>' % (email, verify_url, verify_url)
    try:
        send_mail(subject, '', settings.EMAIL_FROM, ['401208941@qq.com'], html_message=html_message)

    except Exception as e:
        print(e)
        return JsonResponse({"code": 300})  # 邮件发送失败
    return JsonResponse({"code": 200})  # 邮件发送成功


# 接受激活邮件

def re_email(request):
    token = request.GET.get("token")
    try:
        data = signing.loads(token)
    except Exception as e:
        print(e)
        return JsonResponse({"code": 400})  # 解密失败
    else:
        # 从data中取出user_id和email
        email = data.get('email')
        try:
            NewUser.objects.filter(email=email).update(is_active=1)
        except Exception as e:
            print(e)
            return JsonResponse({"code": 300})  # 激活失败
        return JsonResponse({"code": 200})  # 激活成功
