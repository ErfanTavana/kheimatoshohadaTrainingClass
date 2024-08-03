from django.urls import path

from .views import register_class, update_view

urlpatterns = [
    path('register/', register_class, name='register_class_name'),  # مسیر ثبت نام
    path('update/<int:user_id>/', update_view, name='update_name'),
]