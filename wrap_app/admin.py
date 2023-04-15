from django.contrib import admin
from .models import User, Admin,Booking,PurchaseBin,Redeem,AddressUser,ReportIssue



# Register your models here.
admin.site.register(User)
admin.site.register(PurchaseBin)
admin.site.register(Redeem)
admin.site.register(Booking)
admin.site.register(AddressUser)
admin.site.register(Admin)
admin.site.register(ReportIssue)

