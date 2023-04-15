from django.conf import settings
from django.db import models
from datetime import datetime,date
from django.contrib.auth.models import User


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,unique=True)
    email = models.EmailField(unique=True)
    # photo = models.ImageField(upload_to='profile_photos/',default='profile_photos/profile_user.png')
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=50,default='null')
    coins = models.IntegerField(default=0)
    occupation = models.CharField(max_length=20)

    def __str__(self):
        return self.email

class Booking(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE,default=0)
    book_id=  models.AutoField(primary_key=True)
    email = models.EmailField()
    uid = models.IntegerField()
    name = models.CharField(max_length=20,default='null')
    wastetype = models.CharField(max_length=20)
    date = models.DateField(settings.DATE_FORMAT)
    booking_address_title = models.CharField(max_length=20,default='null')
    booking_address = models.CharField(max_length=100,default='null')
    booking_status = models.CharField(max_length=20)
    booking_latitude = models.FloatField(default='0.0')
    booking_longitude = models.FloatField(default='0.0')

    def __str__(self):
        return self.email

class PurchaseBin(models.Model) :
    pid = models.AutoField(primary_key=True)
    email = models.EmailField()
    uid = models.IntegerField()
    name = models.CharField(max_length=20,default='null')
    amount = models.IntegerField()
    address = models.CharField(max_length=50,default='null')
    returnsbin =  models.CharField(max_length=50,default='null')

class Redeem(models.Model) :
    rid = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to='redeem_photos/')
    description = models.CharField(max_length=100)
    CHOICE_ONE = 'trending'
    CHOICE_TWO = 'ongoing'
    MY_CHOICES = [
        (CHOICE_ONE, 'trending'),
        (CHOICE_TWO, 'ongoing'),
    ]
    order_type = models.CharField(max_length=10, choices=MY_CHOICES)
    amount = models.IntegerField()

class AddressUser(models.Model) :
    aid = models.AutoField(primary_key=True)
    email = models.EmailField()
    uid = models.IntegerField()
    name = models.CharField(max_length=20,default='null')
    address_title = models.CharField(max_length=20,default='null')
    address_content = models.CharField(max_length=50,default='null')
    latitude = models.FloatField(default='0.0')
    longitude = models.FloatField(default='0.0')

class ReportIssue(models.Model) :
    email = models.EmailField()
    uid = models.IntegerField()
    name = models.CharField(max_length=20,default='null')
    photo = models.ImageField(upload_to='report_photos/')
    address_report = models.CharField(max_length=50,default='null')


class Admin(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=20)