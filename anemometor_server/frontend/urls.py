
from django.urls import path,include
from . import views

urlpatterns = [
    path(r'httptest/',include(views.http_test())),
]