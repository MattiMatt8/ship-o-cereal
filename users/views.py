from django.shortcuts import render
from django.http import HttpResponse

def something(response):
    return HttpResponse("something_else")