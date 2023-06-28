from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError

class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.RESTRICT,related_name="cities")

    def __str__(self):
        return f"{self.name} city of {self.province.name}"

def numeric_charfield_validator(value : str):
    print(value)
    if not value.isdigit():
        raise ValidationError("This field only accepts numbers.")

class Customer(models.Model):
    firstname = models.CharField(max_length=200, blank=True)
    lastname = models.CharField(max_length=200)
    customertype_choices = [
        (1, "person"),
        (2, "company")
    ]
    customertype = models.IntegerField(choices=customertype_choices, default=0)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, related_name="customers")
    address = models.CharField(max_length=200, blank=True)
    postalcode = models.CharField(max_length=10, validators=[numeric_charfield_validator], blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Contact(models.Model):
    name = models.CharField(max_length=400)
    description = models.CharField(max_length=1000, blank=True)
    phonenumber = PhoneNumberField(blank=True)
    mobilenumber = PhoneNumberField(blank=True)
    faxnumber = PhoneNumberField(blank=True)
    email = models.EmailField(max_length=200, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="contacts")

    def __str__(self):
        return self.name