from django.urls import path,include
from . import views
from .views import posttest

urlpatterns=[
    path("test/",views.test.as_view()),
    path("posttest/",views.posttest),
    path("create/",views.WinddataAPIView.as_view()),
    path("list/",views.WinddataAPIView.as_view()),
    path("DHCP/",views.DHCP.as_view),
]