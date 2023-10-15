
from django.http import HttpResponse

# Create your views here.


def http_test(request):
    return HttpResponse("test")