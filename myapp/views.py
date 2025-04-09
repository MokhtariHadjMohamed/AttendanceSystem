from django.shortcuts import render, redirect
from myapp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
        del request.session['service_id']

    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')

# Admin
# Dashboard


def homeAdmin(request):
    if request.session.get('service_id'):
        return render(request, 'myapp/pages/Error/error-404.html')
    users = None
    try:
        users = User.objects.get(state="absence")
    except User.DoesNotExist:
        error = "Invalid credentials"
        print("error homeadmin get user absence")
    context = {"users": users}

    return render(request, "myapp/index.html", context)

# employee


def showAllEmployees(request):
    if request.session.get('service_id'):
        return render(request, 'myapp/pages/Error/error-404.html')
    users = User.objects.all()
    context = {"users": users}
    return render(request, "myapp/pages/Employees/showAllEmployees.html", context)


def addNewEmployee(request):
    if request.session.get('service_id'):
        return render(request, 'myapp/pages/Error/error-404.html')

    return render(request, "myapp/pages/Employees/addNewEmployees.html")
# section


def showAllSection(request):
    if request.session.get('service_id'):
        return render(request, 'myapp/pages/Error/error-404.html')
    services = Service.objects.all()
    context = {"services": services}
    return render(request, "myapp/pages/Section/showAllSection.html", context)


def addNewSection(request):
    if request.session.get('service_id'):
        return render(request, 'myapp/pages/Error/error-404.html')
    if request.method == "POST":
        try:
            s = Service(request.POST['username'])
            s.save()
        except Service.DoesNotExist:
            error = "Invalid credentials"
            print("error service")
    return render(request, "myapp/pages/Section/addNewSection.html")

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

    return render(request, 'myapp/pages/Office/scanQrCode.html')
