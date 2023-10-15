from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.


def http_test(self,request):
    http='<!DOCTYPE html><html lang="ja">test</html>'
    return HttpResponse(http)