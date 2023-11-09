from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

LHWD=[]

def DictInit():
    
    return True

class WinddataAPIView(APIView):

    def post(self,request):

        return HttpResponse('good')

