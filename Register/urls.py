from django.urls import path

from .views import register_class, update_view, user_login, list_view, list_classes_view, create_class_view, \
    update_class_view

urlpatterns = [
    path('', list_view, name='list'),  # صفحه لیست کاربران
    path('register/', register_class, name='register_class_name'),  # مسیر ثبت نام
    path('update/<int:student_id>/', update_view, name='update_name'),
    path("login/", user_login, name="login"),

    path("create_class/", create_class_view, name="create_class_view_name"),

    path("update_class/<int:class_id>/", update_class_view, name="update_class_view_name"),

    path("list_classes/", list_classes_view, name="list_classes_view_name"),

]
