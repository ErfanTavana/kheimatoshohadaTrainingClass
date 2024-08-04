from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Student
from .models import User, Class
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
import jdatetime


def jalali_to_gregorian(jalali_date_str):

    year, month, day = map(int, jalali_date_str.split('/'))
    jalali_date = jdatetime.date(year, month, day)
    gregorian_date = jalali_date.togregorian()
    return gregorian_date.strftime('%Y-%m-%d')

def register_class(request):
    if not request.user.is_authenticated:
        pass
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
        birth_date = jalali_to_gregorian(birth_date)

        payment_amount = request.POST.get('payment_amount')
        contact_number = request.POST.get('contact_number')

        # گرفتن کلاس‌های انتخاب شده
        class_ids = request.POST.getlist('classes')
        classes = Class.objects.all()

        # اعتبارسنجی داده‌ها (اختیاری)
        if not first_name or not last_name or not national_code or not birth_date:
            return render(request, 'Register/register.html',
                          context={'classes': classes, 'error': 'لطفا فیلد های ضروری را تکمیل کنید'})
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
            classes = Class.objects.filter(id__in=class_ids)
            student.classes.set(classes)

            return redirect('update_name', student_id=student.id)
        except ValueError as e:
            return render(request, 'Register/register.html',
                          context={'classes': classes, 'error': f'{str(e)}'})
        except Exception as e:
            print(e)
            return render(request, 'Register/register.html',
                          context={'classes': classes, 'error': 'خطا در ثبت نام لطفا دوباره تلاش کنید'})


def update_view(request, student_id):
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

#
# def list_basiji(request):
#     if request.user.is_authenticated:
#         kol_age = 0
#         cunt = 0
#         Money = 0
#         price = 0
#         price_2 = 0
#         registrations = RegisterForSummerClasses.objects.all()
#         if registrations.count() == 0:
#             return render(request, 'basiji/list.html', {'registrations': registrations.order_by("-id")})
#         for user in registrations:
#             kol_age += user.age
#             cunt += 1
#             Money += user.payment_amount
#             price += user.price
#             price_2 += user.price_2
#         Average = kol_age / cunt
#         Average = int(Average)
#
#         return render(request, 'basiji/list.html',
#                       {'registrations': registrations.order_by("-id"), "Average": Average, "Money": Money,
#                        "price": price,
#                        "price_2": price_2})
#     else:
#         return redirect("login")
#
#
# def update_user(request, id):
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             name = request.POST.get('name')
#             last_name = request.POST.get('last_name')
#             if len(name) < 2 and len(last_name) < 2:
#                 return render(request, 'basiji/register.html')
#             else:
#                 father_name = request.POST.get("father_name")
#                 national_code = request.POST.get("national_code")
#                 birthdate = request.POST.get("birthdate")
#                 jalali_date_list = birthdate.split("/")
#                 j_year, j_month, j_day = map(int, jalali_date_list)
#                 miladi_date = JalaliDate(j_year, j_month, j_day).to_gregorian().strftime("%Y-%m-%d")
#                 payment_amount = request.POST.get("payment_amount")
#                 phone_number = request.POST.get("phone_number")
#                 Urdu = request.POST.get("Urdu") is not None
#                 consent_letter = request.POST.get("consent_letter") is not None
#                 photoshop = request.POST.get("photoshop") is not None
#                 python = request.POST.get("python") is not None
#                 futsal = request.POST.get("futsal") is not None
#                 swim = request.POST.get("swim") is not None
#                 self_defense = request.POST.get("self_defense") is not None
#                 shooting = request.POST.get("shooting") is not None
#                 relief_and_rescue = request.POST.get("relief_and_rescue") is not None
#                 biology = request.POST.get("biology") is not None
#                 photography = request.POST.get("photography") is not None
#                 military_tactics = request.POST.get("military_tactics") is not None
#                 rhetorical = request.POST.get("rhetorical") is not None
#                 robotic = request.POST.get("robotic") is not None
#                 math = request.POST.get("math") is not None
#                 quran = request.POST.get("quran") is not None
#                 english = request.POST.get("english") is not None
#                 arabic = request.POST.get("arabic") is not None
#                 try:
#                     print(id)
#                     registration = RegisterForSummerClasses.objects.get(id=id)
#                     registration.name = name
#                     registration.last_name = last_name
#                     registration.father_name = father_name
#                     registration.national_code = national_code
#                     registration.birthdate = miladi_date
#                     registration.payment_amount = payment_amount
#                     registration.phone_number = phone_number
#                     registration.Urdu = Urdu
#                     registration.consent_letter = consent_letter
#                     registration.photoshop = photoshop
#                     registration.python = python
#                     registration.futsal = futsal
#                     registration.swim = swim
#                     registration.self_defense = self_defense
#                     registration.shooting = shooting
#                     registration.relief_and_rescue = relief_and_rescue
#                     registration.biology = biology
#                     registration.photography = photography
#                     registration.military_tactics = military_tactics
#                     registration.rhetorical = rhetorical
#                     registration.robotic = robotic
#                     registration.math = math
#                     registration.quran = quran
#                     registration.english = english
#                     registration.arabic = arabic
#                     registration.save()
#                 except RegisterForSummerClasses.DoesNotExist:
#                     registration = RegisterForSummerClasses(name=name, last_name=last_name, father_name=father_name,
#                                                             national_code=national_code, birthdate=miladi_date,
#                                                             payment_amount=payment_amount, phone_number=phone_number,
#                                                             Urdu=Urdu,consent_letter=consent_letter,photoshop=photoshop, python=python, futsal=futsal,
#                                                             swim=swim,
#                                                             self_defense=self_defense, shooting=shooting,
#                                                             relief_and_rescue=relief_and_rescue, biology=biology,
#                                                             photography=photography, military_tactics=military_tactics,
#                                                             rhetorical=rhetorical, robotic=robotic, math=math,
#                                                             quran=quran, english=english, arabic=arabic)
#                     registration.save()
#         print('+++')
#         user = RegisterForSummerClasses.objects.get(id=id)
#         return render(request, 'basiji/update.html', {"user": user})
#     else:
#         return redirect("login")
#
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
    if request.user.is_authenticated == True:
        return redirect("register_class_name")
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
