from django.contrib import admin

from .models import *
from .views import *

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "province")

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "firstname", "lastname", "customertype", "city", "address", "postalcode")
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "phonenumber", "mobilenumber", "faxnumber", "email", "customer")


