from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from .models import User, Admin,Booking,AddressUser,Redeem,PurchaseBin,ReportIssue

#loader and home\
def loader(request):
    return render(request,'loader.html')
def get_start(request):
    return render(request,'get_start.html')
def select_occupation(request):
    return render(request,'select_occupation.html')
