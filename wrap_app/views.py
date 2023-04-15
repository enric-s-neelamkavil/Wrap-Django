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

#user registration
def signup(request):
    if request.method == 'GET':
        occupation = request.GET['occupation']
        return render(request, 'signup.html', {'occupation': occupation})
    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('email')
        # photo = request.FILES.get('photo')
        occupation = request.POST.get('occupation')
        password = request.POST.get('password')
        re_password = request.POST.get('repassword')

        if(password == re_password):
            print(occupation)
            # user = User(name=name,email=email,photo=photo,password=password)
            user = User(name=name,email=email,password=password,occupation=occupation)
            user.save()
            email = [email]
            request.session['uname'] = name
            request.session['email'] = email
            request.session['occupation'] = occupation
            if occupation=='User':
                return dashboard(request)
            elif occupation=='Employee':
                return render(request, 'employee/dashboard.html')
            elif occupation == 'Company':
                return render(request, 'managers/profile.html')
            data = {'status':"Password and Re-entered password must be same"}
            return render(request,'signup.html',context=data)
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.get(name=name,email=email)
        print(user.occupation)
        occupation = user.occupation
        if user.password == password:
            request.session['uname'] = name
            request.session['email'] = email
            if occupation=='User':
                return dashboard(request)
            elif occupation=='Employee':
                return render(request, 'employee/dashboard.html')
            elif occupation == 'Company':
                return render(request, 'managers/profile.html')
        else:
            data = {'status':"Incorrect Password!!!"}
            return render(request,'signin.html',context=data)
    else:
        return render(request, 'signin.html')