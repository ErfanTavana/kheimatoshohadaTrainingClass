from django.urls import path

from .views import register_class

urlpatterns = [
    path('register/', register_class, name='register_class_name'),
]
