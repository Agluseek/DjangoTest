from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from StudyDjango.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    return render(request, 'index.html')


# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            response = HttpResponseRedirect('/event_manage/')
            request.session['user'] = username  # 将信息记录到浏览器
            return HttpResponseRedirect('/event_manage/')
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


# 发布会管理
@login_required
def event_manage(request):
    username = request.session.get('user', '')
    event_list = Event.objects.all()
    return render(request, "event_manage.html", {"user": username, "events": event_list})


# 搜索名字
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数 ,取第一页面数据
        contacts = paginator.page(1)
        # 如果page不在范围，取最后一页面
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})

@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request ,'sign_index.html', {'event': event})