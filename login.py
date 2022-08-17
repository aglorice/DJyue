import time
from io import BytesIO


import ddddocr
from PIL import Image
import binascii
import rsa
import base64
import requests
from bs4 import BeautifulSoup
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from urllib import parse


class Login(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.key_url = parse.urljoin(base_url, '/xtgl/login_getPublicKey.html')
        self.login_url = parse.urljoin(base_url, '/xtgl/login_slogin.html')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': self.login_url}
        self.sess = requests.Session()
        self.sess.keep_alive = False
        self.cookies = ''
        self.cookies_str = ''

    def get_pinfo(self):
        """获取个人信息"""

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': self.base_url}

        url = parse.urljoin(self.base_url, '/xsxxxggl/xsxxwh_cxCkDgxsxx.html?gnmkdm=N100801')

        res = self.sess.get(url, headers=headers)
        jres = res.json()
        res_dict = {
            'name': jres['xm'],
            'studentId': jres['xh'],
            'brithday': jres['csrq'],
            'idNumber': jres['zjhm'],
            'candidateNumber': jres['ksh'],
            'status': jres['xjztdm'],
            'collegeName': jres['zsjg_id'],
            'majorName': jres['zyh_id'],
            'className': jres['bh_id'],
            'entryDate': jres['rxrq'],
            'graduationSchool': jres['byzx'],
            # 'domicile': jres['hkszd'],
            'politicalStatus': jres['zzmmm'],
            'national': jres['mzm'],
            'education': jres['pyccdm'],
            'postalCode': jres['yzbm']
        }
        return res_dict

    def re_check_code(self):
        url = "https://jwxt.xcc.edu.cn/kaptcha"
        res = self.sess.get(url=url)
        image = Image.open(BytesIO(res.content))
        ocr = ddddocr.DdddOcr()
        yzm = ocr.classification(res.content)
        return yzm, image

    def csrf_token(self):
        req = self.sess.get(self.login_url, headers=self.headers, timeout=5)
        soup = BeautifulSoup(req.text, 'html')
        print(req.text)
        try:
            tokens = soup.find(id='csrftoken').get("value")
        except Exception as e:
            return 1
        return tokens

    def key_password(self, password):
        res = self.sess.get(self.key_url, headers=self.headers).json()

        n = res['modulus']
        e = res['exponent']

        hmm = self.get_rsa(password, n, e)
        return hmm

    def yzm(self):
        self.sess.get(self.login_url, headers=self.headers, timeout=3)
        yzm, img = self.re_check_code()
        print("识别的验证码为" + str(yzm))
        return yzm, img

    def login(self, sid, tokens, hmm, yzm):
        """登陆"""
        # 获取csrf_token
        print(sid, tokens, hmm, yzm)
        login_data = {'csrftoken': tokens,
                      'yhm': sid,
                      'mm': hmm,
                      'mm': hmm,
                      'yzm': yzm}
        url = self.login_url
        res = self.sess.post(url, headers=self.headers, data=login_data)
        if "验证码输入错误！" in res.text:
            return 0
        elif "用户名或密码不正确，请重新输入！" in res.text:
            return 1
        self.cookies = self.sess.cookies

        self.cookies_str = '; '.join([item.name + '=' + item.value for item in self.cookies])
        return 2

    def get_grade(self, year, term):
        """获取成绩"""
        url = parse.urljoin(self.base_url, '/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        elif term == '0':
            term = ''
        else:
            print('Please enter the correct term value！！！ ("0" or "1" or "2")')
            return {}
        data = {
            'xnm': year,  # 学年数
            'xqm': term,  # 学期数，第一学期为3，第二学期为12, 整个学年为空''
            '_search': 'false',
            'nd': int(time.time() * 1000),
            'queryModel.showCount': '100',  # 每页最多条数
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '0'  # 查询次数
        }
        res = self.sess.post(url=url, headers=self.headers, data=data)
        jres = res.json()
        if jres.get('items'):  # 防止数据出错items为空
            res_dict = {
                'name': jres['items'][0]['xm'],
                'studentId': jres['items'][0]['xh'],
                'schoolYear': jres['items'][0]['xnm'],
                'schoolTerm': jres['items'][0]['xqmmc'],
                'course': [{
                    'courseTitle': i['kcmc'],
                    'teacher': i['jsxm'],
                    'courseId': i['kch_id'],
                    # 'className': i['jxbmc'],
                    'courseNature': '' if i.get('kcxzmc') == None else i.get('kcxzmc'),
                    'credit': i['xf'],
                    'grade': i['cj'],
                    'gradePoint': '' if i.get('jd') == None else i.get('jd'),
                    'gradeNature': i['ksxz'],
                    'startCollege': i['kkbmmc'],
                    'courseMark': i['kcbj'],
                    'courseCategory': i['kclbmc'],
                    'courseAttribution': '' if i.get('kcgsmc') == None else i.get('kcgsmc'),
                    'xwkc':i['sfxwkc']
                } for i in jres['items']]}
            return res_dict
        else:
            return {}

    def get_message(self):
        """获取消息"""
        url = parse.urljoin(self.base_url, '/xtgl/index_cxDbsy.html?doType=query')
        data = {
            'sfyy': '0',  # 是否已阅，未阅未1，已阅为2
            'flag': '1',
            '_search': 'false',
            'nd': int(time.time() * 1000),
            'queryModel.showCount': '1000',  # 最多条数
            'queryModel.currentPage': '1',  # 当前页数
            'queryModel.sortName': 'cjsj',
            'queryModel.sortOrder': 'desc',  # 时间倒序, asc正序
            'time': '0'
        }
        try:
            res = self.sess.get(url, headers=self.headers, data=data,timeout=3)
        except Exception as e:
            return {'err': 'Connect Timeout'}
        jres = res.json()
        res_list = [{'message': i.get('xxnr'), 'ctime': i.get('cjsj')} for i in jres.get('items')]
        return res_list

    def get_schedule(self, year, term):
        """获取课程表信息"""
        # 'http://jwc.xhu.edu.cn/kbcx/xskbcx_cxXsShcPdf.html?doType=list&xnm=2019&xqm=3&xszd.sj=true&xszd.cd=true&xszd.js=true&xszd.jszc=false&xszd.jxb=true&xszd.xkbz=true&xszd.kcxszc=true&xszd.zhxs=true&xszd.zxs=true&xszd.khfs=true&xszd.xf=true&xnmc=2019-2020&xqmmc=1&xm=%25E5%25BB%2596%25E6%2596%2587%25E8%25B1%25AA&jgmc=undefined&xxdm=&gnmkdm=N2151'
        url = parse.urljoin(self.base_url, '/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        else:
            print('Please enter the correct term value！！！ ("1" or "2")')
            return {}
        data = {
            'xnm': year,
            'xqm': term
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
        jres = res.json()
        res_dict = {
            'name': jres['xsxx']['XM'],
            'studentId': jres['xsxx']['XH'],
            'schoolYear': jres['xsxx']['XNM'],
            'schoolTerm': jres['xsxx']['XQMMC'],
            'normalCourse': [{
                'courseTitle': i['kcmc'],
                'teacher': i['xm'],
                'courseId': i['kch_id'],
                'courseSection': i['jc'],
                'courseWeek': i['zcd'],
                'campus': i['xqmc'],
                'courseRoom': i['cdmc'],
                'className': i['jxbmc'],
                'hoursComposition': i['kcxszc'],
                'weeklyHours': i['zhxs'],
                'totalHours': i['zxs'],
                'credit': i['xf']
            } for i in jres['kbList']],
            'otherCourses': [i['qtkcgs'] for i in jres['sjkList']]}
        return res_dict

    # 切断会话
    def loginout(self):
        self.sess.close()
        print(self.sess.cookies)


    @classmethod
    def get_rsa(cls, pwd, n, e):
        """对密码base64编码"""
        message = str(pwd).encode()
        rsa_n = binascii.b2a_hex(binascii.a2b_base64(n))
        rsa_e = binascii.b2a_hex(binascii.a2b_base64(e))
        key = rsa.PublicKey(int(rsa_n, 16), int(rsa_e, 16))
        encropy_pwd = rsa.encrypt(message, key)
        result = binascii.b2a_base64(encropy_pwd)
        return result
