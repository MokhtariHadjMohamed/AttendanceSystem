from django.urls import path

from . import views

urlpatterns = [
    #  LogIn
    path("", views.login, name="login"),
    path('logout/', views.logout_view, name='logout'),
    # AdminSection
    path("homeAdmin", views.homeAdmin, name="homeAdmin"),
    
    path("showAllEmployees", views.showAllEmployees, name="showAllEmployees"),
    path("addNewEmployee", views.addNewEmployee, name="addNewEmployee"),
    
    path("showAllSection", views.showAllSection, name="showAllSection"),
    path("addNewSection", views.addNewSection, name="addNewSection"),
    # Service Screen
    path("scanFace", views.scanFace, name="scanFace"),
    path("scanFigerPrint", views.scanFigerPrint, name="scanFigerPrint"),
    path("scanQrCode", views.scanQrCode, name="scanQrCode")
]