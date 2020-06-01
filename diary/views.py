# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from icecream import ic

from diary.models import Diary

import datetime

request_get_from = 0
history = ""


# Create your views here.
@csrf_exempt
def diary(request):
    global request_get_from
    global history

    date = recorded_dates = weekday = ""
    total_days = 0
    editor0 = editor1 = editor2 = editor3 = editor4 = editor5 = ""
    y_count = m_count = w_count = total_count = excepts = 0
    weekday_array = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

    if request.method == "POST":
        if request.POST.get('history') is None:
            date = request.POST['date']
            weekday = request.POST['weekday']
            total_days = str(int(request.POST['total_days']) + 1)
            editor0 = request.POST['eidtor0'].strip()
            editor1 = request.POST['eidtor1'].strip()
            editor2 = request.POST['eidtor2'].strip()
            editor3 = request.POST['eidtor3'].strip()
            editor4 = request.POST['eidtor4'].strip()
            editor5 = request.POST['eidtor5'].strip()
            y_count = str(int(request.POST['y_count']) + 1)
            m_count = str(int(request.POST['m_count']) + 1)
            w_count = str(int(request.POST['w_count']) + 1)
            d = Diary(date=date, weekday=weekday, total_days=total_days, editor0=editor0, editor1=editor1,
                      editor2=editor2, editor3=editor3, editor4=editor4, editor5=editor5, y_count=y_count,
                      m_count=m_count, w_count=w_count)
            d.save()
            request_get_from = 1
        else:
            history = request.POST.get('history')
            request_get_from = 2

    if request.method == "GET":
        recorded_dates = getRecordedDates()
        if request_get_from == 1:
            today = getToday()
            (date, weekday, total_days, editor0, editor1, editor2, editor3, editor4, editor5,
             y_count, m_count, w_count, excepts) = getHistoryDiaryRecord(today)
            weekday = weekday_array[datetime.date.today().weekday()]
            total_count = getTotalCount(date)
            request_get_from = 1
        elif request_get_from == 2:
            (date, weekday, total_days, editor0, editor1, editor2, editor3, editor4, editor5,
             y_count, m_count, w_count, excepts) = getHistoryDiaryRecord(history)
            total_count = getTotalCount(history)
            request_get_from = 2
        else:
            today = getToday()
            (date, weekday, total_days, editor0, editor1, editor2, editor3, editor4, editor5,
             y_count, m_count, w_count, excepts) = getHistoryDiaryRecord(today)
            weekday = weekday_array[datetime.date.today().weekday()]
            if excepts == 1:
                date, total_days, editor0, editor1, editor2, y_count, m_count, w_count, excepts = getLastDirayRecord()
                excepts += 1
                if date != "":
                    dt = str(date)
                    last_day = datetime.date(int(dt[:4]), int(dt[5:7]), int(dt[8:10]))
                    diff_days = (datetime.date.today() - last_day).days
                    if diff_days >= 365:
                        editor0 = editor1 = editor2 = ""
                        y_count = m_count = w_count = 0
                    elif diff_days >= 28:
                        editor1 = editor2 = ""
                        m_count = w_count = 0
                    elif diff_days >= 7:
                        editor2 = ""
                        w_count = 0
            total_count = getTotalCount(today)
            request_get_from = 2
        request_get_from = 0
        context = {'date': history, 'weekday': weekday,
                   'total_days': total_days, 'request_get_from': request_get_from,
                   'y_count': y_count, 'm_count': m_count, 'w_count': w_count,
                   'editor0': editor0, 'editor1': editor1,
                   'editor2': editor2, 'editor3': editor3, 'editor4': editor4,
                   'editor5': editor5, 'total_count': total_count,
                   'excepts': excepts, 'recorded_dates': recorded_dates}
        ic(context)
        return render(request, 'diary.html', context=context)
    return render(request, 'diary.html')


def getHistoryDiaryRecord(dt):
    try:
        dy = Diary.objects.get(date=dt)
        date = dy.date
        weekday = dy.weekday
        total_days = dy.total_days
        editor0, editor1, editor2, editor3, editor4, editor5 = \
            dy.editor0, dy.editor1, dy.editor2, dy.editor3, dy.editor4, dy.editor5
        y_count, m_count, w_count = dy.y_count, dy.m_count, dy.w_count
        return (
            date, weekday, total_days,
            editor0, editor1, editor2, editor3, editor4, editor5,
            y_count, m_count, w_count, 0)
    except Exception as e:
        print(e)
        return (
            "", "", 0,
            "", "", "", "", "", "",
            0, 0, 0, 1
        )


def getLastDirayRecord():
    try:
        dy = Diary.objects.order_by("-date")[0]
        date = dy.date
        total_days = dy.total_days
        editor0 = dy.editor0.strip()
        editor1 = dy.editor1.strip()
        editor2 = dy.editor2.strip()
        # 今日计划
        # editor3 = dy.editor5.strip()
        y_count, m_count, w_count = dy.y_count, dy.m_count, dy.w_count
        return date, total_days, editor0, editor1, editor2, y_count, m_count, w_count, 0
    except Exception as e:
        print(e)
        return (
            "", 0,
            "", "", "", "", "", "",
            0, 0, 0, 1
        )


def getTotalCount(ld):
    try:
        dy = Diary.objects.order_by("date")[0]
        dt = str(dy.date)
        first_day = datetime.date(int(dt[:4]), int(dt[5:7]), int(dt[8:10]))  # 2015年09月06日
        ld = str(ld)
        last_day = datetime.date(int(ld[:4]), int(ld[5:7]), int(ld[8:10]))
        total_count = (last_day - first_day).days
        return total_count + 1
    except Exception as e:
        print(e)
        return 0


def getToday():
    td = str(datetime.date.today())
    td = td.split('-')
    return td[0] + u'年' + td[1] + u'月' + td[2] + u'日'


def formatDate(dt):
    dt = str(dt)
    fdt = dt[:4]
    fdt += '-'
    fdt += dt[5:7].lstrip('0')
    fdt += '-'
    fdt += dt[8:10].lstrip('0')
    return fdt


def getRecordedDates():
    recorded_dates = ""
    diary_list = Diary.objects.all()
    for dl in diary_list:
        recorded_dates += formatDate(dl.date) + " "
    return recorded_dates
