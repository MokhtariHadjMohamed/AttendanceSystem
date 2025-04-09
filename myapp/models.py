from django.db import models

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    nmrTlp = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class User(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    nmrTlp = models.CharField(max_length=10)
    prenom = models.CharField(max_length=200)
    timeIn = models.DateTimeField("time in")
    timeOut = models.DateTimeField("time Out")
    salare = models.BigIntegerField(default=0)
    typeUser = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=200)
    fingerPritn = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Appointmetn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    checkIn = models.DateTimeField("check in")
    checkOut = models.DateTimeField("check out")
    data_appointment = models.DateTimeField("date appointment")