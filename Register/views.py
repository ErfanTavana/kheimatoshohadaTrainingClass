from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Student
from .models import User, Class
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
import jdatetime

from django.shortcuts import render
from .models import Student, Class
from django.db.models import Sum, Avg
from django.shortcuts import render
from .models import Student, Class
from django.db.models import Sum, Avg


def jalali_to_gregorian(jalali_date_str):
    year, month, day = map(int, jalali_date_str.split('/'))
    jalali_date = jdatetime.date(year, month, day)
    gregorian_date = jalali_date.togregorian()
    return gregorian_date.strftime('%Y-%m-%d')


def register_class(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'GET':
        classes = Class.objects.all()
        return render(request, 'Register/register.html', context={"classes": classes})

    if request.method == 'POST':
        # گرفتن داده‌های فرم
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        father_name = request.POST.get('father_name')
        national_code = request.POST.get('national_code')
        birth_date = request.POST.get('birth_date')
        if birth_date:
            birth_date = jalali_to_gregorian(birth_date)
        else:
            birth_date = '2006-03-11'
        payment_amount = request.POST.get('payment_amount')
        contact_number = request.POST.get('contact_number')

        # گرفتن کلاس‌های انتخاب شده
        class_ids = request.POST.getlist('classes')
        classes = Class.objects.all()

        # اعتبارسنجی داده‌ها
        if not first_name or not last_name or not national_code or not birth_date:
            return render(request, 'Register/register.html',
                          context={
                              'classes': classes,
                              'first_name': first_name,
                              'last_name': last_name,
                              'father_name': father_name,
                              'national_code': national_code,
                              'birth_date': birth_date,
                              'payment_amount': payment_amount,
                              'contact_number': contact_number,
                              'classes_ids': class_ids,
                              'error': 'لطفا فیلد های ضروری را تکمیل کنید'
                          })

        try:
            # ایجاد یک دانش‌آموز جدید
            student = Student.objects.create(
                user=request.user,  # ارتباط با کاربر وارد شده
                first_name=first_name,
                last_name=last_name,
                father_name=father_name,
                national_code=national_code,
                birth_date=birth_date,
                payment_amount=payment_amount,
                contact_number=contact_number
            )

            # اضافه کردن کلاس‌های انتخاب شده به دانش‌آموز
            selected_classes = Class.objects.filter(id__in=class_ids)
            student.classes.set(selected_classes)

            return redirect('update_name', student_id=student.id)
        except ValueError as e:
            return render(request, 'Register/register.html',
                          context={
                              'classes': classes,
                              'first_name': first_name,
                              'last_name': last_name,
                              'father_name': father_name,
                              'national_code': national_code,
                              'birth_date': birth_date,
                              'payment_amount': payment_amount,
                              'contact_number': contact_number,
                              'classes_ids': class_ids,
                              'error': f'{str(e)}'
                          })
        except Exception as e:
            print(e)
            return render(request, 'Register/register.html',
                          context={
                              'classes': classes,
                              'first_name': first_name,
                              'last_name': last_name,
                              'father_name': father_name,
                              'national_code': national_code,
                              'birth_date': birth_date,
                              'payment_amount': payment_amount,
                              'contact_number': contact_number,
                              'classes_ids': class_ids,
                              'error': 'خطا در ثبت نام لطفا دوباره تلاش کنید'
                          })

def update_view(request, student_id):
    if not request.user.is_authenticated:
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.father_name = request.POST.get('father_name')
        student.national_code = request.POST.get('national_code')

        # Convert birth_date to YYYY-MM-DD format
        birth_date = request.POST.get('birth_date')
        birth_date = jalali_to_gregorian(birth_date)

        student.birth_date = birth_date

        student.payment_amount = int(request.POST.get('payment_amount') or 0)
        student.contact_number = request.POST.get('contact_number')

        class_ids = request.POST.getlist('classes')
        student.classes.set(Class.objects.filter(id__in=class_ids))

        student.save()
        return redirect('update_name', student_id=student.id)

    classes = Class.objects.all()
    student_classes = student.classes.values_list('id', flat=True)

    # Calculate the total cost of the selected classes
    total_class_cost = sum(class_obj.class_cost for class_obj in student.classes.all())

    # Calculate the remaining amount to be paid
    remaining_amount = total_class_cost - student.payment_amount

    # Prepare context for rendering
    context = {
        'student': student,
        'classes': classes,
        'student_classes': student_classes,
        'remaining_amount': remaining_amount,
    }

    return render(request, 'Register/update.html', context)


from django.db.models import Avg, F, ExpressionWrapper, IntegerField
from django.shortcuts import render, redirect
from django.db.models import Sum
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import Student, Class
from django.db.models import Sum
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import Student, Class


def list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    students = Student.objects.all()
    classes = Class.objects.all()

    name_search = request.GET.get('name_search')
    last_name_search = request.GET.get('last_name_search')
    class_ids = request.GET.get('classes')  # باید به صورت لیست دریافت شود

    if name_search:
        students = students.filter(first_name__icontains=name_search)
    if last_name_search:
        students = students.filter(last_name__icontains=last_name_search)
    if class_ids:
        # برای فیلتر کردن بر اساس کلاس‌ها
        students = students.filter(classes__id__in=class_ids).distinct()

    # محاسبه هزینه کلاس‌ها و مبلغ قابل پرداخت برای هر کاربر
    student_data = []
    for student in students:
        total_class_cost = student.classes.aggregate(total_cost=Sum('class_cost'))['total_cost'] or 0
        remaining_amount = total_class_cost - student.payment_amount
        student_data.append({
            'student': student,
            'total_class_cost': total_class_cost,
            'remaining_amount': remaining_amount
        })

    # محاسبه میانگین سنی
    now = datetime.now()
    ages = [student.age for student in students]  # استفاده از property age
    average_age = sum(ages) / len(ages) if ages else 0

    context = {
        'students_data': student_data,
        'classes': classes,
        'Money': sum(data['student'].payment_amount for data in student_data),
        'price': sum(data['total_class_cost'] for data in student_data),
        'price_2': sum(data['remaining_amount'] for data in student_data),
        'Average': average_age,
    }

    return render(request, 'Register/list.html', context)


#
# def list_basiji_search(request):
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             kol_age = 0
#             cunt = 0
#             Money = 0
#             price = 0
#             price_2 = 0
#             name_search = request.POST.get("name_search")
#             last_name_search = request.POST.get("last_name_search")
#             idd = request.POST.get("idd")
#             registrations = RegisterForSummerClasses.objects.all()
#             name_search = name_search.strip()
#             name_search = name_search.rstrip()
#             last_name_search = last_name_search.strip()
#             last_name_search = last_name_search.lstrip()
#             # اعمال فیلتر بر اساس مقادیر ورودی سرچ
#             if name_search:
#                 registrations = registrations.filter(name__icontains=name_search)
#             if last_name_search:
#                 registrations = registrations.filter(last_name__icontains=last_name_search)
#             if idd and idd != "انتخاب کنید...":
#                 filter_kwargs = {}
#                 filter_kwargs[f"{idd}"] = True
#                 registrations = registrations.filter(**filter_kwargs)
#             if registrations.count() == 0:
#                 return render(request, 'basiji/list.html', {'registrations': registrations.order_by("-id")})
#             for user in registrations:
#                 kol_age += user.age
#                 cunt += 1
#                 Money += user.payment_amount
#                 price += user.price
#                 price_2 += user.price_2
#             Average = kol_age / cunt
#             Average = int(Average)
#
#             return render(request, 'basiji/list.html',
#                           {'registrations': registrations.order_by("-id"), "Average": Average, "Money": Money,
#                            "price": price,
#                            "price_2": price_2})
#         return redirect('list')
#     else:
#         return redirect("login")
#
#
def user_login(request):
    if request.user.is_authenticated:
        return redirect("list")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=f"{username}", password=f"{password}")
        if user is not None:
            login(request, user)
            return redirect('register_class_name')
        else:
            return render(request, "Register/login.html", context={"eroor": 'نام كاربري يا رمز عبور اشتباه است'})
    # f = RegisterForSummerClasses.objects.all()
    # for i in f :
    #     print(i.national_code)
    #     i.quran = True
    #     i.quran = False
    #     i.save()
    return render(request, "Register/login.html")
