from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from .models import User, Admin,Booking,AddressUser,Redeem,PurchaseBin,ReportIssue

import folium
from django.conf import settings
import os
import geocoder

#loader and home\
def loader(request):
    return render(request,'loader.html')
def get_start(request):
    return render(request,'get_start.html')
def select_occupation(request):
    return render(request,'select_occupation.html')


# Admin pages

def admin_home(request):
    if 'aname' in request.session:
        data = {'name':request.session.get('aname')}
        return render(request,'admin_home.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'admin_login.html',context=data)
    
def login_admin(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = Admin.objects.get(name=name)

            if user.password == password:
                request.session['aname'] = name
                # return HttpResponse('ffaf')
                return admin_home(request)
            else:
                data = {'status':"Incorrect Password!!!"}
                return render(request,'admin_login.html',context=data)

        except Exception as e:
            data = {'status':"Invalid Username"}
            return render(request,'admin_login.html',context=data)
    else:
        return HttpResponse("Something went wrong faffsffa!!!!!")


def admin_logout(request):
    if 'aname' in request.session:
        del request.session['aname']

    return render(request,'admin_login.html')

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



def user_logout(request):
    if 'uname' in request.session:
        del request.session['uname']

    return render(request,'loader.html')

#User Home Page
def dashboard(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        return render(request,'users/dashboard.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
month=["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]   
def booking(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        name = request.session.get('uname')
        email = request.session.get('email')
        bookings = Booking.objects.all()
        print(email,name)
        users  = User.objects.get(name=request.session['uname'])
        bookings = Booking.objects.all() # Get all Booking objects from the database
        booking_data = []
        count=0
        for booking in bookings:
            if booking.uid == users.uid:
                if booking.booking_status == 'Booked' and count==0:
                    count=1
                booking_data.append({'book_id':booking.book_id,'name': booking.name, 'email': booking.email, 'uid': booking.uid,'wastetype':booking.wastetype,'date':str(booking.date),'date1':str(booking.date)[8:10],'month':month[int(str(booking.date)[5:7])-1],'booking_status':booking.booking_status})
        return render(request,'users/booking.html',{'bookings': booking_data,'count':count})
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)

def delete_booking(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        if request.method == 'POST':
            book_id = request.POST.get('book_id')
            books = Booking.objects.filter(book_id=book_id)
            print(books,book_id)
            books.delete()
            return redirect('booking')
        return render(request,'users/booking.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)

      
def rewards(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        return render(request,'users/rewards.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)

def redeem(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        users  = User.objects.get(name=request.session['uname'])
        redeem = Redeem.objects.all()
        redeem_data = []
        for red in redeem:
            print(red.amount,red.description)
            # image_path = os.path.join(settings.BASE_DIR, red.photo)
            # with open(image_path, 'rb') as f:
            #     image_data = f.read()
            # redeem_data.append({'photo':image_data,'description':red.description,'amount':red.amount,'order_type':red.order_type})
            redeem_data.append({'photo':red.photo,'description':red.description,'amount':red.amount,'order_type':red.order_type})
            print(red.photo)
        my_dict = {
                'coins':users.coins
            }
        return render(request,'users/redeem.html',{'my_dict':my_dict,'redeem':redeem_data})
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)
    
def track(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        m = folium.Map(location=[10.307897806699529,76.33507993927475], zoom_start=12)
        folium.Marker(location=[10.527627837215208, 76.21445706825584], popup="<p>Waste picked up</p>",
                  tooltip="11 AM", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker(location=[10.512665164588398, 76.25561768977308], popup="<p>Reached collection point</p>",
                  tooltip="04:03 PM", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker(location=[10.380721708232917, 76.2974580261964], popup="<p>Sent to Infinite waste LLC</p>",
                  tooltip="05:59 PM", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker(location=[10.307003287734428, 76.33404101823123], popup="<p>On the way</p>",
                  tooltip="Just now", icon=folium.Icon(color="green")).add_to(m)
        trail_coordinates = [
            (10.527627837215208, 76.21445706825584),
            (10.523402028044528, 76.21676339524682),
            (10.519703423024081, 76.23536899988589),
            (10.516517757310858, 76.23639896810602),
            (10.512243214395411, 76.24628360262749),
            (10.512665164588398, 76.25561768977308),
            (10.511230531485214, 76.25838572952064),
            (10.44553925741713, 76.25895097511498),
            (10.438250590627376, 76.26464509672473),
            (10.434547789578632, 76.26604183367157),
            (10.413445049777307, 76.27076760239916),
            (10.394643441226956, 76.28688595976858),
            (10.387101170763309, 76.28899028286708),
            (10.383513125885708, 76.29289557903502),
            (10.380721708232917, 76.2974580261964),
            (10.371372889255452, 76.30409791447754),
            (10.370526874778777, 76.30986345834272),
            (10.371289720024908, 76.30407888007696),
            (10.370635399487753, 76.30944329789006),
            (10.367757892786981, 76.31390110718998),
            (10.357267374074375, 76.31662623143903),
            (10.351337316076425, 76.31821067557871),
            (10.34830617592037, 76.32067779967979),
            (10.341336158809888, 76.3223738294376),
            (10.337283183792525, 76.32153698025876),
            (10.32652276578376, 76.32295778284612),
            (10.31912449146524, 76.32680047441302),
            (10.311481803371343, 76.3310774898666),
            (10.307003287734428, 76.33404101823123)

        ]
        folium.PolyLine(trail_coordinates, tooltip="Coast",color="darkred").add_to(m)
        m = m._repr_html_()
        return render(request,'users/track.html',{ "m": m})
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)
    
#dashboard pages
def dropoff(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        if request.method == 'POST':
            users  = User.objects.get(name=request.session['uname'])
            print(users.email)
            wastetype = request.POST.get('wastetype')
            date = request.POST.get('date')
            booking_address = request.POST.get('booking_address')
            print(date)
            book = Booking(wastetype=wastetype,name=users.name,uid=users.uid ,date=date,email=users.email, booking_address=booking_address,booking_status="In-Transit")
            book.save()
            return render(request,'dashboard/success/dropoff-success.html',context=data)
        return render(request,'users/dashboard/dropoff.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)
    
def pickup(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        users  = User.objects.get(name=request.session['uname'])
        adr = AddressUser.objects.filter(uid=users.uid)

        if request.method == 'POST':
            print(users.email)
            wastetype = request.POST.get('wastetype')
            date = request.POST.get('date')
            booking_address_title = request.POST.get('booking_address_title')
            booking_address = request.POST.get('booking_address')
            booking_latitude = request.POST.get('booking_latitude')
            booking_longitude = request.POST.get('booking_longitude')
            print(date)
            book = Booking(wastetype=wastetype,name=users.name,uid=users.uid ,date=date,email=users.email, booking_address=booking_address,booking_status="Booked",booking_address_title=booking_address_title,booking_latitude=booking_latitude,booking_longitude=booking_longitude)
            book.save()
            return render(request,'users/dashboard/success/pickup-success.html',context=data)
        return render(request,'users/dashboard/pickup.html',{"context":data,'adr':adr})
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)
    
def purchase(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        if request.method == 'POST':
            return render(request,'users/dashboard/success/purchase-success.html',context=data)
        return render(request,'users/dashboard/purchase.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)
    
def report(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        if request.method == 'POST':
            return render(request,'users/dashboard/success/report-success.html',context=data)
        return render(request,'users/dashboard/report.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)

def profile(request):
    if request.method == 'POST':
        user= User()
        user.name = request.POST.get('uname')
        user.email = request.POST.get('email')
        # user.photo = request.FILES.get('photo')
        users  = User.objects.get(name=request.session['uname'])
        data = {'name':request.session.get('uname')}
        # if user.photo:
        #     user.photo = request.FILES.get('photo')
        # user = User(name=name,email=email,photo=user.photo)
        # user = User(name=name,email=email)
        user.save()
        return redirect('profile')
    else:
         if 'uname' in request.session:
            # name = request.session.get('uname')
            # email = request.session.get('email')
            users  = User.objects.get(name=request.session['uname'])

            # password = {'name':request.session.get('password')}
            my_dict = {
                'name': users.name,
                'email':users.email,
                'occupation':users.occupation,
                'coins':users.coins
            }
            return render(request,'users/profile.html',{'my_dict':my_dict,'occupation':users.occupation})
         else:
            data = {'status':'You need to login first'}
            return render(request,'signin.html',context=data)


#notification
def notification(request):
    if 'uname' in request.session:
        return render(request,'users/notification.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)


#user-profile pages   
def edit_profile(request):
    if 'uname' in request.session:
        users  = User.objects.get(name=request.session['uname'])
        my_dict = {
                'name': users.name,
                'email':users.email,
                'password':users.password,
                'coins':users.coins
            }
        if request.method == 'POST':
            users  = User.objects.get(name=request.session['uname'])
            print(users.name)
            name = request.POST.get('new_name')
            email = request.POST.get('new_email')
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new1_password = request.POST.get('new1_password')
            print(name,email)
            if old_password == users.password and new1_password==new_password and new_password != '':
                # us = User(name=name,email=email,password=new_password)
                # us.save()
                users.name=name
                users.email=email
                users.password=new1_password
                uname=name
                users.save()
            elif old_password == users.password :
                us = User(name=name,email=email)
                uname=name
                us.save()
            # return redirect('profile',uname)
            return redirect('signin')

        user = User.objects.get(name=request.session['uname'])
        if user.occupation == "User":
            return render(request,'users/profile/edit-profile.html',my_dict)
        elif user.occupation == "Employee":
            return render(request,'employee/profile/edit-profile.html',my_dict)
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)
    
def support_profile(request):
    if 'uname' in request.session:
        user = User.objects.get(name=request.session['uname'])
        if user.occupation == "User":
            return render(request,'users/profile/support-profile.html')
        elif user.occupation == "Employee":
            return render(request,'employee/profile/support-profile.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)
    
def contact_us(request):
    if 'uname' in request.session:
        user = User.objects.get(name=request.session['uname'])
        if user.occupation == "User":
            return render(request,'users/profile/contact-us.html')
        elif user.occupation == "Employee":
            return render(request,'employee/profile/contact-us.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)
def delete_user(request):
    if 'uname' in request.session:
        user = User.objects.get(name=request.session['uname'])
        if request.method == 'POST':
            user = User.objects.get(name=request.session['uname'])
            books = Booking.objects.filter(uid=user.uid)
            print(books)
            books.delete()
            user.delete()
            return redirect('signin')
        if user.occupation == "User":
            return render(request,'users/profile/delete-user.html')
        elif user.occupation == "Employee":
            return render(request,'employee/profile/delete-user.html')

    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)
    
def add_address(request):
    if 'uname' in request.session:
        latitude = 'null'
        longitude = 'null'
        user = User.objects.get(name=request.session['uname'])
        adr = AddressUser.objects.filter(uid=user.uid)
        if request.method == 'POST':  
            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')
            address_title = request.POST.get('address_title')
            address_content = request.POST.get('address_content')
            g = geocoder.ip('me')
            latitude = g.lat
            longitude = g.lng
            print(longitude,latitude,address_content,address_title)
            print(adr)
            adrs = AddressUser(uid=user.uid,email=user.email,name=user.name,address_title=address_title,address_content=address_content,latitude=latitude,longitude=longitude)
            print(adrs)
            adrs.save()
            # return render(request,'users/profile/add-address.html',{'lat':latitude,'log':longitude})
            return redirect('add_address')
        return render(request,'users/profile/add-address.html',{'lat':latitude,'log':longitude,'adr':adr})
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)
def delete_address(request):
    if 'uname' in request.session:
        user = User.objects.get(name=request.session['uname'])
        if request.method == 'POST':  
            address_title = request.POST.get('address_title')
            address_content = request.POST.get('address_content')
            aid = request.POST.get('aid')
            adr = AddressUser.objects.filter(aid=aid)
            print(adr)
            adr.delete()
            return redirect('add_address')
        return render(request,'users/profile/add-address.html',{'adr':adr})
    else:
        data = {'status':'You need to login first'}
        return render(request,'signin.html',context=data)

#Employee pages
def dashboard_employee(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        return render(request,'employee/dashboard.html',context=data)
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def pending_pickups(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        return redirect(paper_pickup)
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def plastic_pickup(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        books = Booking.objects.all()
        booking_data=[]
        for book in books:
            if book.wastetype=='Plastic waste':
                print(book)
                booking_data.append({'name': book.name, 'email': book.email, 'uid': book.uid,'wastetype':book.wastetype,'date':str(book.date),'date1':str(book.date)[8:10],'booking_status':book.booking_status,'address':book.booking_address,'book_id':book.book_id})
        return render(request,'employee/plastic-pickup.html',{'booking':booking_data})
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def biowaste_pickup(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        books = Booking.objects.all()
        booking_data=[]
        if request.method == 'POST':
            wastetype = request.POST.get('wastetype')
            book_id = request.POST.get('book_id')
            kg = request.POST.get('kilo')
            if kg != 'None':
                print(book_id,wastetype,kg)
                coins = int(kg)*50
                # coin = calculate_wrap_coins(wtype,kg)
                print(coins)
                print("hello")

        for book in books:
            if book.wastetype=='Bio waste':
                print(book)
                booking_data.append({'name': book.name, 'email': book.email, 'uid': book.uid,'wastetype':book.wastetype,'date':str(book.date),'date1':str(book.date)[8:10],'booking_status':book.booking_status,'address':book.booking_address,'book_id':book.book_id})
        return render(request,'employee/biowaste-pickup.html',{'booking':booking_data})
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def paper_pickup(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        books = Booking.objects.all()
        booking_data=[]
        for book in books:
            if book.wastetype=='Paper or clipboard':
                print(book)
                booking_data.append({'name': book.name, 'email': book.email, 'uid': book.uid,'wastetype':book.wastetype,'date':str(book.date),'date1':str(book.date)[8:10],'booking_status':book.booking_status,'address':book.booking_address,'book_id':book.book_id})
        return render(request,'employee/paper-pickup.html',{'booking':booking_data})
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def glass_pickup(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        books = Booking.objects.all()
        booking_data=[]
        for book in books:
            if book.wastetype=='Glass waste':
                print(book)
                booking_data.append({'name': book.name, 'email': book.email, 'uid': book.uid,'wastetype':book.wastetype,'date':str(book.date),'date1':str(book.date)[8:10],'booking_status':book.booking_status,'address':book.booking_address,'book_id':book.book_id})
        return render(request,'employee/glass-pickup.html',{'booking':booking_data})
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def ewaste_pickup(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        books = Booking.objects.all()
        booking_data=[]
        for book in books:
            if book.wastetype=='e-waste':
                print(book)
                booking_data.append({'name': book.name, 'email': book.email, 'uid': book.uid,'wastetype':book.wastetype,'date':str(book.date),'date1':str(book.date)[8:10],'booking_status':book.booking_status,'address':book.booking_address,'book_id':book.book_id})
        return render(request,'employee/ewaste-pickup.html',{'booking':booking_data})
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def others_pickup(request):
    if 'uname' in request.session:
        data = {'name':request.session.get('uname')}
        books = Booking.objects.all()
        booking_data=[]
        for book in books:
            if book.wastetype=='others':
                print(book)
                booking_data.append({'name': book.name, 'email': book.email, 'uid': book.uid,'wastetype':book.wastetype,'date':str(book.date),'date1':str(book.date)[8:10],'booking_status':book.booking_status,'address':book.booking_address,'book_id':book.book_id})
        return render(request,'employee/others-pickup.html',{'booking':booking_data})
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def employee_profile(request):
    if request.method == 'POST':
        user= User()
        user.name = request.POST.get('uname')
        user.email = request.POST.get('email')
        users  = User.objects.get(name=request.session['uname'])
        data = {'name':request.session.get('uname')}
        user.save()
        return redirect('employee_profile')
    else:
         if 'uname' in request.session:
            users  = User.objects.get(name=request.session['uname'])
            my_dict = {
                'name': users.name,
                'email':users.email,
                'occupation':users.occupation,
                'coins':users.coins
            }
            return render(request,'employee/employee_profile.html',{'my_dict':my_dict,'occupation':users.occupation})
         else:
            data = {'status':'You need to login first'}
            return render(request,'signin.html',context=data)

def calculate_wrap_coins(wtype,kg):
    if wtype == 'Bio waste':
        coins = 50*kg
    elif wtype == 'Plastic waste':
        coins = 100*kg
    elif wtype == 'Glass waste':
        coins = 70*kg
    elif wtype == 'Paper or clipboard':
        coins = 150*kg
    elif wtype == 'e-waste':
        coins = 125*kg
    elif wtype == 'others':
        coins = 25*kg
    return (coins)

def routeway(request):
    if 'uname' in request.session:
        return render(request,'employee/routeway-pages/paper-routeway.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def complaint(request):
    if 'uname' in request.session:
        return render(request,'employee/complaint.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)

def ewaste_routeway(request):
    if 'uname' in request.session:
        return render(request,'employee/routeway-pages/ewaste-routeway.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
        
def biowaste_routeway(request):
    if 'uname' in request.session:
        return render(request,'employee/routeway-pages/biowaste-routeway.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def glass_routeway(request):
    if 'uname' in request.session:
        return render(request,'employee/routeway-pages/glass-routeway.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)

def others_routeway(request):
    if 'uname' in request.session:
        return render(request,'employee/routeway-pages/others-routeway.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def paper_routeway(request):
    if 'uname' in request.session:
        return render(request,'employee/routeway-pages/paper-routeway.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def plastic_routeway(request):
    if 'uname' in request.session:
        return render(request,'employee/routeway-pages/plastic-routeway.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)
    
def tensorflow_scan(request):
    if 'uname' in request.session:
        return render(request,'users/scan.html')
    else:
        data = {'status':'You need to login first'}
        return render(request,'sigin.html',context=data)