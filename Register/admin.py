from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'father_name', 'national_code', 'birth_date', 'payment_amount', 'contact_number')
    search_fields = ('first_name', 'last_name', 'national_code')
    filter_horizontal = ('classes',)  # اضافه کردن یک فیلد چند انتخابی برای کلاس‌ها

    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name', 'father_name', 'national_code', 'birth_date', 'payment_amount', 'contact_number')
        }),
        ('Classes', {
            'fields': ('classes',),
            'description': 'Choose classes that the student is enrolled in.'
        }),
    )
from django.contrib import admin
from .models import Class

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'class_cost')
    search_fields = ('class_name',)
    list_filter = ('class_cost',)

    fieldsets = (
        (None, {
            'fields': ('class_name', 'class_cost')
        }),
    )
