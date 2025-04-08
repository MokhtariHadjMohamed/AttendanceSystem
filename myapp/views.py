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


def logout_view(request):
    if 'service_id' in request.session:
        del request.session['service_id']

    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')  # Redirect to login page after logging out

# Admin
# Dashboard


def homeAdmin(request):
    return render(request, "myapp/index.html")

# employee


def showAllEmployees(request):
    return render(request, "myapp/pages/Employees/showAllEmployees.html")


def addNewEmployee(request):
    return render(request, "myapp/pages/Employees/addNewEmployees.html")
# section


def showAllSection(request):
    return render(request, "myapp/pages/Section/showAllSection.html")


def addNewSection(request):
    return render(request, "myapp/pages/Section/addNewSection.html")

# Service Section


def scanFace(request):
    return render(request, 'myapp/pages/Office/scanFace.html')


def scanFigerPrint(request):
    return render(request, 'myapp/pages/Office/scanFigerPrint.html')


def scanQrCode(request):
    return render(request, 'myapp/pages/Office/scanQrCode.html')
