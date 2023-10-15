from django.urls import path
from . import views

urlpatterns = [
    path('create/',views.WinddataAPIView.as_view()),
    path('list/',views.listdata.as_view()),
    path('anemometor/',views.AnemometorAIPView.as_view()),
    path('DHCP/',views.DHCP.as_view())
]