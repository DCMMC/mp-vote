"""vote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import subprocess
from datetime import timezone
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static
import json
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from openpyxl import load_workbook
from background_task import background
from .models import Works, UserVoteLog
import os

# deploy_domain = '142.93.185.148:8888'
deploy_domain = '192.168.1.103:8080'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'code': 'success'
            })
        else:
            return JsonResponse({'code': 'error'})
    else:
        return HttpResponseForbidden()


def generate_pdf(url, tag):
    print('开始处理 ' + tag + ': ' + url)
    subprocess.run(['bash', os.path.join(BASE_DIR,
                                         '..',
                                         'weixinCapture',
                                         'generate_pdf.sh'),
                    url])
    print('完成处理 ' + tag + ': ' + url)
    return 'http://' + deploy_domain + '/media/' + tag + '.pdf'


@background(schedule=0)
def process_works(works, max_votes, sheet, idx):
    while True:
        tag = sheet['A' + idx]
        if tag is not None:
            works[tag] = {
                'tag': tag,
                'title': sheet['B' + idx],
                'desc': sheet['C' + idx],
                'imageURL': sheet['D' + idx],
                'origin_url': sheet['E' + idx],
                'pdf_url': generate_pdf(sheet['E' + idx], tag),
                'votes': 0
            }
            idx += 1
        else:
            break
    if len(Works.objects.all()) > 0:
        Works.objects.all()[0].delete()
    w = Works(works=json.dumps(works))
    w.max_votes = max_votes
    w.save()


@login_required
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        max_votes = request.POST.get('max_votes', 1)
        works = request.FILE['file']
        with open('temp_works.xlsx', 'wb+') as f:
            for chunk in works.chunks():
                f.write(chunk)
        wb = load_workbook(filename='temp_works.xlsx')
        sheet = wb['Sheet1']
        valid = all([
            sheet['A1'].value == '作品 id',
            sheet['B1'].value == '作品名称',
            sheet['C1'].value == '作品简介',
            sheet['D1'].value == '图片简介',
            sheet['E1'].value == '作品链接'
        ])
        if valid:
            idx = 2
            works = {}
            process_works(works, max_votes, sheet, idx,
                          schedule=timezone.now())
            return JsonResponse({'code': 'success', 'data': len(works.keys())})
        else:
            return JsonResponse({
                'code': 'error',
                'data': '文件格式错误, 必须按照模板文件,!'
            })
    else:
        return HttpResponseForbidden()


@csrf_exempt
@login_required
def get_results(request):
    if request.method == 'POST':
        if len(Works.objects.all()) > 0:
            works = json.loads(Works.objects.all()[0].works)
            return JsonResponse({
                'code': 'success',
                'data': works
            })
        else:
            return JsonResponse({'code': 'error', 'data': '还未上传作品列表!'})
    else:
        return HttpResponseForbidden()


@csrf_exempt
def vote(req):
    if req.method == 'POST':
        user_id = req.POST.get('user_id', None)
        tag = req.POST.get('tag', None)
        if user_id and tag:
            u = UserVoteLog.objects.filter(wechat_openid=user_id)
            max_votes = Works.objects.all()[0].max_votes
            if len(u) >= max_votes:
                return JsonResponse({'code': 'error', 'data': '您已经投过了!'})
            else:
                log = UserVoteLog()
                log.work_tag = tag
                log.wechat_openid = user_id
                log.save()
                works = Works.objects.all()[0]
                works_obj = json.loads(works.works)
                works_obj['tag']['votes'] += 1
                works.works = json.dumps(works_obj)
                works.save()
                return JsonResponse({'code': 'success'})
        else:
            return JsonResponse({'code': 'error'})
    else:
        return HttpResponseForbidden()


@csrf_exempt
def get_works(req):
    if req.method == 'POST':
        works = Works.objects.all()
        if len(works) > 0:
            user_id = req.POST.get('userId', None)
            if user_id:
                works = works[0]
                max_votes = works.max_votes
                works = works.works
                u = UserVoteLog.objects.filter(wechat_openid=user_id)
                for work in works:
                    works[work]['voted'] = False
                if len(u) > 0:
                    for vote in u:
                        works[vote.work_tag]['voted'] = True
                return JsonResponse({
                    'code': 'success',
                    'data': {
                        'works': works,
                        'max_votes': max_votes
                    }
                })
            else:
                return JsonResponse({
                    'code': 'error'
                })
        else:
            return JsonResponse({
                'code': 'error',
                'data': '当前没有作品可供投票'
            })
    else:
        return HttpResponseForbidden()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminLogin', admin_login),
    path('get_results', get_results),
    path('vote', vote),
    path('getWorks', get_works),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
