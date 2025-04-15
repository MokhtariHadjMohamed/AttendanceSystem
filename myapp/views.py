from django.shortcuts import render, redirect
from myapp.models import *
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
import json
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, time
from collections import defaultdict


# LogIn


def login(request):
    if request.session.get('service_id'):
        return redirect('scanQrCode')

    if request.session.get('user_id'):
        return redirect('homeAdmin')

    if request.method == "POST":
        try:
            s = Service.objects.get(username=request.POST['username'],
                                    password=request.POST['password'])
            request.session['service_id'] = s.id
            s.state = "open"
            s.save()
            return redirect('scanQrCode')
        except Service.DoesNotExist:
            error = "Invalid credentials"
            print("error service")

        try:
            u = User.objects.get(username=request.POST['username'],
                                 password=request.POST['password'])
            request.session['user_id'] = u.id
            return redirect('homeAdmin')
        except User.DoesNotExist:
            error = "Invalid credentials"
            print("error service")

    return render(request, "myapp/pages/Auth/login.html", None)


def logout(request):
    if 'service_id' in request.session:
        s = Service.objects.get(
            id=request.session['service_id'])
        s.state = "close"
        s.save()
        del request.session['service_id']

    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')

# Admin
# Dashboard


def homeAdmin(request):
    if request.session.get('service_id'):
        return render(request, 'myapp/pages/Error/error-404.html')
    appointment = None
    try:
        appointment = Appointmetn.objects.all()
    except User.DoesNotExist:
        error = "Invalid credentials"
        print("error homeadmin get appointmetn absence")
    context = {"appointments": appointment,
               "name": User.objects.get(id=request.session.get('user_id'))}

    return render(request, "myapp/index.html", context)

# employee


def showAllEmployees(request):
    if request.session.get('service_id'):
        return render(request, 'myapp/pages/Error/error-404.html')

    status = request.GET.get('status')
    if status:
        users = User.objects.filter(state=status)
    else:
        users = User.objects.all()

    search = request.GET.get("query")
    if search:
        users = User.objects.filter(name=search)
    else:
        users = User.objects.all()

    report = []
    for user in users:
        print(user.calculate_salary())
        report.append({
            "user": user,
            "calculated_salary": user.calculate_salary(),
        })

    context = {"report": report,
                "name": User.objects.get(id=request.session.get('user_id')),
                }
    
    return render(request, "myapp/pages/Employees/showAllEmployees.html", context)


def addNewEmployee(request):
    if request.session.get('service_id'):
        return render(request, 'myapp/pages/Error/error-404.html')
    if request.method == 'POST':
        try:
            timeOut_str = f"2025-04-12 {request.POST['TimeOut']}"
            timeOut = datetime.strptime(timeOut_str, "%Y-%m-%d %H:%M")

            timeIn_str = f"2025-04-12 {request.POST['TimeIn']}"
            timeIn = datetime.strptime(timeIn_str, "%Y-%m-%d %H:%M")

            user = User(name=request.POST['Name'], state='absent',
                        username=request.POST['Username'], password=request.POST['Password'],
                        address=request.POST['Address'], nmrTlp=request.POST['PhoneNumber'],
                        prenom=request.POST['Prenom'], timeIn=timeIn,
                        timeOut=timeOut, salare=request.POST['Salare'],
                        typeUser=request.POST['userType'], imageUrl="url",
                        fingerPritn="123",
                        service=Service.objects.get(id=request.POST['idServie']))
            user.save()
            return redirect('showAllEmployees')
        except Service.DoesNotExist:
            error = "Invalid credentials"
            print("error Add Employee")
    services = Service.objects.all()
    context = {"services": services,
               "name": User.objects.get(id=request.session.get('user_id'))}
    return render(request, "myapp/pages/Employees/addNewEmployees.html", context=context)
# section


def showAllSection(request):
    if request.session.get('service_id'):
        return render(request, 'myapp/pages/Error/error-404.html')
    services = Service.objects.all()

    search = request.GET.get("query")
    if search:
        services = Service.objects.filter(name=search)
    else:
        services = Service.objects.all()

    context = {"services": services,
               "name": User.objects.get(id=request.session.get('user_id'))}
    return render(request, "myapp/pages/Section/showAllSection.html", context)


def addNewSection(request):
    if request.session.get('service_id'):
        return render(request, 'myapp/pages/Error/error-404.html')
    if request.method == "POST":
        try:
            s = Service(name=request.POST['Name'], state='close',
                        username=request.POST['Username'], password=request.POST['Password'],
                        address=request.POST['Address'], nmrTlp=request.POST['PhoneNumber'])
            s.save()
            return redirect('showAllSection')

        except Service.DoesNotExist:
            error = "Invalid credentials"
            print("error service")

    context = {"name": User.objects.get(id=request.session.get('user_id'))}
    return render(request, "myapp/pages/Section/addNewSection.html", context=context)

# Service Section


def scanFace(request):
    if request.session.get('user_id'):
        return render(request, 'myapp/pages/Error/error-404.html')

    return render(request, 'myapp/pages/Office/scanFace.html')


def scanFigerPrint(request):
    if request.session.get('user_id'):
        return render(request, 'myapp/pages/Error/error-404.html')

    return render(request, 'myapp/pages/Office/scanFigerPrint.html')


def scanQrCode(request):
    if request.session.get('user_id'):
        return render(request, 'myapp/pages/Error/error-404.html')

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            raw_code = data.get('code')

            code = json.loads(raw_code)
            username = code.get('username')
            password = code.get('password')

            u = User.objects.get(
                username=username, password=password)
            u.state = 'presant'

            s = Service.objects.get(
                id=request.session['service_id']
            )

            now = datetime.now()
            date_only = now.strftime("%Y-%m-%d")
            time_only = now.strftime("%H:%M:%S")

            morning_start = datetime.strptime(
                f"{date_only} 08:00:00", "%Y-%m-%d %H:%M:%S")
            morning_end = datetime.strptime(
                f"{date_only} 12:00:00", "%Y-%m-%d %H:%M:%S")

            afternoon_start = datetime.strptime(
                f"{date_only} 13:00:00", "%Y-%m-%d %H:%M:%S")
            afternoon_end = datetime.strptime(
                f"{date_only} 17:00:00", "%Y-%m-%d %H:%M:%S")

            if morning_start <= now <= morning_end:
                pointing(date_only, time_only, u, s, "08:00:00")
            elif afternoon_start <= now <= afternoon_end:
                pointing(date_only, time_only, u, s, "13:00:00")

        except Exception as e:
            print(f'error scan qrcode: {e}')

    return render(request, 'myapp/pages/Office/scanQrCode.html')


def pointing(date, time, user, service, houer):
    a = Appointmetn.objects.filter(
        data_appointment=datetime.strptime(
            f"{date} {houer}", "%Y-%m-%d %H:%M:%S"),
        checkOut=datetime.strptime(
            f"{date} 00:00:00", "%Y-%m-%d %H:%M:%S"),
        user=user)

    if a:
        a.update(checkOut=datetime.strptime(
            f"{date} {time}", "%Y-%m-%d %H:%M:%S"))
        user.state = 'absent'
        user.save()
    else:
        a = Appointmetn(user=user, service=service,
                        checkIn=datetime.strptime(
                            f"{date} {time}", "%Y-%m-%d %H:%M:%S"),
                        checkOut=datetime.strptime(
                            f"{date} 00:00:00", "%Y-%m-%d %H:%M:%S"),
                        data_appointment=datetime.strptime(f"{date} {houer}", "%Y-%m-%d %H:%M:%S"))
        a.save()
        user.state = 'presant'
        user.save()


def getDataInOneDay(request):
    data = {
        "absent": 0,
        "presant": 0
    }

    try:
        u_absent = User.objects.filter(state="absent")
        u_presant = User.objects.filter(state="presant")

        data = {
            "absent": len(u_absent),
            "presant": len(u_presant)
        }
    except:
        print("error get data")

    return JsonResponse(data)


def getDataInOneWeek(request):
    today = timezone.now().date()
    one_week_ago = today - timedelta(days=6)

    appointments = Appointmetn.objects.filter(
        data_appointment__date__range=(one_week_ago, today))

    week_data = defaultdict(lambda: {"present": 0, "late": 0, "absent": 0})

    attended_users = set()

    for appointment in appointments:
        date_str = appointment.data_appointment.strftime("%Y-%m-%d")
        user_id = appointment.user.id
        attended_users.add((user_id, date_str))

        check_in_time = appointment.checkIn.time()
        if check_in_time > time(9, 0):
            week_data[date_str]["late"] += 1
        else:
            week_data[date_str]["present"] += 1

    all_users = User.objects.all()

    for i in range(7):
        day = today - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")

        for user in all_users:
            if (user.id, day_str) not in attended_users:
                week_data[day_str]["absent"] += 1

    return JsonResponse(dict(week_data))
