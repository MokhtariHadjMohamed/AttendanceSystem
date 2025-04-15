from django.db import models
from django.utils import timezone
import calendar

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
    
    def calculate_salary(self, month=None, year=None):
        """
        Calculate salary for a specific month/year based on attendance.
        Defaults to the current month/year.
        """
        # Determine month/year
        now = timezone.now()
        month = month if month else now.month
        year = year if year else now.year

        # Get total days in the month
        _, total_days = calendar.monthrange(year, month)

        # Count days the user had appointments (days present)
        days_present = Appointmetn.objects.filter(
            user=self,
            data_appointment__month=month,
            data_appointment__year=year
        ).count()

        # Calculate salary proportion (e.g., salary = base_salary * (days_present / total_days))
        if total_days == 0:
            return 0  # Avoid division by zero
        return (self.salare / total_days) * days_present

class Appointmetn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    checkIn = models.DateTimeField("check in")
    checkOut = models.DateTimeField("check out")
    data_appointment = models.DateTimeField("date appointment")