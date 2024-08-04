from django.contrib.auth.models import User
from django.db import models
from django.db import models
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students', blank=True, null=True)
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    father_name = models.CharField(max_length=50, verbose_name="نام پدر")
    national_code = models.CharField(max_length=10, unique=True, verbose_name="کد ملی")
    birth_date = models.DateField(verbose_name="تاریخ تولد")
    payment_amount = models.IntegerField(blank=True, null=True, default=0, verbose_name="مبلغ پرداخت شده")
    contact_number = models.CharField(max_length=15, verbose_name="تلفن تماس")
    classes = models.ManyToManyField('Class', related_name='students', verbose_name="کلاس‌ها")
    @property
    def age(self):
        today = datetime.today()
        return relativedelta(today, self.birth_date).years

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Class(models.Model):
    class_name = models.CharField(max_length=100, verbose_name="نام کلاس")
    class_cost = models.IntegerField(blank=True, null=True, default=0, verbose_name="هزینه کلاس")

    def __str__(self):
        return self.class_name
