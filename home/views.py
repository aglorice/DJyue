import datetime
import io
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from mainApp.views import check_login
from login import *

base_url = 'https://jwxt.xcc.edu.cn/'  # 教务系统的地址

# 登录教务系统


lgn = Login(base_url=base_url)


# Create your views here.
@check_login
def index(request):
    global lgn

    if request.method == "GET":
        lgn = Login(base_url=base_url)
        return render(request, "home_index/home_index.html")
    elif request.method == "POST":
        student_id = request.POST.get("student_id")
        password = request.POST.get("password")
        yzm = request.POST.get("check-code")
        tokens = lgn.csrf_token()
        if tokens == 1:
            return HttpResponseRedirect('/home/info_zfxt')
        hmm = lgn.key_password(password)
        state = lgn.login(sid=student_id, tokens=tokens, hmm=hmm, yzm=yzm)
        if state == 0 or state == 1:
            return render(request, "home_index/home_index.html", locals())

        # data = lgn.get_schedule('2022', '1')
        # print(data)
        return HttpResponseRedirect('/home/info_zfxt')


@check_login
def new_yzm(request):
    yzm, im = lgn.yzm()
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    request.session['yzm'] = yzm
    return HttpResponse(buf.getvalue(), 'image/png')


@check_login
def check_code(request):
    yzm = request.session['yzm']
    return JsonResponse({"yzm": yzm})


@check_login
def info_zfxt(request):
    return render(request, "home_index/info-zfxt.html", locals())


@check_login
def loginout(request):
    lgn.loginout()
    return HttpResponseRedirect('/home/index')


@check_login
def get_pinfo(request):
    data = lgn.get_pinfo()
    # data['entryDate'] = data['entryDate'].split("-")[0]
    return JsonResponse(data)


@check_login
def get_message(request):
    msg = lgn.get_message()
    return JsonResponse(msg, safe=False)


@check_login
def get_grade(request):
    data = {}
    data_x = []
    data_2 = []

    year = int(request.GET.get("year"))
    term = int(request.GET.get("month"))
    zylb = int(request.GET.get("zylb"))
    if term == 0:
        year -= 1
        term += 1
    else:
        term -= 1
    year = str(year)
    term = str(term + 1)
    msg = lgn.get_grade(year, term)
    msg = msg['course']

    for i in range(len(msg)):
        if zylb == 3:  # 全部成绩
            data_x.append(msg[i]['courseTitle'])
            if msg[i]['grade'] == "优":
                msg[i]['grade'] = 100
            data_2.append({
                "value": msg[i]['grade'],
                "gradePoint": msg[i]['gradePoint'],
                'teacher': msg[i]['teacher']
            })

            data = {
                "x": data_x,
                "nb": data_2,
                "zylb": "全部成绩"
            }
        elif zylb == 2:  # 专业成绩

            if msg[i]['courseNature'] == "专业教育":
                data_x.append(msg[i]['courseTitle'])
                data_2.append({
                    "value": msg[i]['grade'],
                    "gradePoint": msg[i]['gradePoint'],
                    'teacher': msg[i]['teacher']
                })

            data = {
                "x": data_x,
                "nb": data_2,
                "zylb": "专业成绩"
            }
        elif zylb == 1:

            if msg[i]['xwkc'] == "是":
                data_x.append(msg[i]['courseTitle'])
                data_2.append({
                    "value": msg[i]['grade'],
                    "gradePoint": msg[i]['gradePoint'],
                    'teacher': msg[i]['teacher']
                })

            data = {
                "x": data_x,
                "nb": data_2,
                "zylb": "学位成绩"
            }

    return JsonResponse(data, safe=False)
