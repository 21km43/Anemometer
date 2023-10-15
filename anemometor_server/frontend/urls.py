
from django.urls import path,include
from . import views

urlpatterns = [
    path(r'http_test/',include(views.http_test)),
]