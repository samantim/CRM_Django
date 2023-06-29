from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


# Create your views here.

def index(request : HttpRequest):
    return render(request, "phonebook/index.html")


def provinces(request : HttpRequest):
    return render(request, "phonebook/provinces.html",{
        "provinces" : Province.objects.all()
    })

class NewProvinceForm(forms.Form):
    name = forms.CharField(max_length=100, min_length=1, label="Name")

def add_province(request: HttpRequest):
    if request.method == "POST":
        validation_form = NewProvinceForm(request.POST)
        if validation_form.is_valid():
            name = validation_form.cleaned_data["name"]
            phonecode = validation_form.cleaned_data["phonecode"]
            province = Province(name = name, phonecode= phonecode)
            province.save()
            return HttpResponseRedirect(reverse("phonebook:provinces"))
        else:
            return render(request, "phonebook/add_province.html", {
                "form" : validation_form
            })
    return render(request, "phonebook/add_province.html",{
        "form" : NewProvinceForm()
    })


def cities(request : HttpRequest):
    return render(request, "phonebook/cities.html",{
        "cities" : City.objects.all()
    })

class NewCityForm(forms.Form):
    name = forms.CharField(max_length=100, min_length=1, label="Name")
    province = forms.ModelChoiceField(queryset=Province.objects.all(), required=True, empty_label="select a province")

def add_city(request: HttpRequest):
    if request.method == "POST":    
        validation_form = NewCityForm(request.POST)
        if validation_form.is_valid():
            name = validation_form.cleaned_data["name"]
            province = validation_form.cleaned_data["province"]
            city = City(name = name, province = province)
            city.save()
            return HttpResponseRedirect(reverse("phonebook:cities"))
        else:
            return render(request, "phonebook/add_city.html", {
                "form" : validation_form
            })
    return render(request, "phonebook/add_city.html",{
        "form" : NewCityForm()
    })

def numeric_charfield_validator(value : str):
    print(value)
    if not value.isdigit():
        raise ValidationError("This field only accepts numbers.")

class NewCustomerForm(forms.Form):
    firstname = forms.CharField(max_length=200, label="First name", required=False)
    lastname = forms.CharField(max_length=200, min_length=1, label="Last name")
    customertype_choices = [
        (1, "person"),
        (2, "company")
    ]
    customertype = forms.ChoiceField(choices=customertype_choices)
    city = forms.ModelChoiceField(City.objects.all(), required=True, empty_label="Select a city")
    address = forms.CharField(max_length=200, widget=forms.Textarea(attrs={"rows":3}), required=False)
    postalcode = forms.CharField(max_length=10, validators=[numeric_charfield_validator], required=False)

def customers(request : HttpRequest):
    return render(request, "phonebook/customers.html",{
        "customers" : Customer.objects.all()
    })

def add_customer(request : HttpRequest):
    if request.method == "POST":
        validation_form = NewCustomerForm(request.POST)
        if validation_form.is_valid():
            firstname = validation_form.cleaned_data["firstname"]
            lastname = validation_form.cleaned_data["lastname"]
            customertype = validation_form.cleaned_data["customertype"]
            city = validation_form.cleaned_data["city"]
            address = validation_form.cleaned_data["address"]
            postalcode = validation_form.cleaned_data["postalcode"]
            customer = Customer(
                firstname = firstname,
                lastname = lastname,
                customertype = customertype,
                city = city,
                address = address,
                postalcode = postalcode
            )
            customer.save()
            return HttpResponseRedirect(reverse("phonebook:customers"))
        else:
            return render(request, "phonebook/add_customer.html",{
                "form" : validation_form
            })

    return render(request, "phonebook/add_customer.html",{
        "form" : NewCustomerForm()
    })

def customer_by_id(request : HttpRequest, customer_id : int):
    return render(request, "phonebook/customer.html", {
        "customer" : Customer.objects.filter(id = customer_id).first()
    })

def contacts(request: HttpRequest, customer_id : int):
    customer = Customer.objects.get(pk = customer_id)
    return render(request, "phonebook/contacts.html",{
        "contacts" : Contact.objects.filter(customer = customer).all(),
        "customer" : customer
    })

class NewContactForm(forms.Form):
    name = forms.CharField(max_length=400, min_length=1)
    description = forms.CharField(max_length=1000, required=False, widget=forms.Textarea(attrs={"rows" : 5}))
    phonenumber = PhoneNumberField(region="IR",
                                    widget=PhoneNumberPrefixWidget(
                                    country_choices=[
                                    ("IR", "Iran"),
                                    ("US", "United Satates"),
                                    ("DE", "Germany")]
                                    ))
    mobilenumber = PhoneNumberField(region="IR",
                                    widget=PhoneNumberPrefixWidget(
                                    country_choices=[
                                    ("IR", "Iran"),
                                    ("US", "United Satates"),
                                    ("DE", "Germany")]
                                    ))
    faxnumber = PhoneNumberField(region="IR",
                                    widget=PhoneNumberPrefixWidget(
                                    country_choices=[
                                    ("IR", "Iran"),
                                    ("US", "United Satates"),
                                    ("DE", "Germany")]
                                    ))
    email = forms.EmailField(max_length=200, required=False)
    
def add_contact(request : HttpRequest, customer_id : int):
    customer = Customer.objects.get(pk = customer_id)
    if request.method == "POST":
        validation_form = NewContactForm(request.POST)
        if validation_form.is_valid():
            name = validation_form.cleaned_data["name"]
            description = validation_form.cleaned_data["description"]
            phonenumber = validation_form.cleaned_data["phonenumber"]
            mobilenumber = validation_form.cleaned_data["mobilenumber"]
            faxnumber = validation_form.cleaned_data["faxnumber"]
            email = validation_form.cleaned_data["email"]
            contact = Contact(
                name = name,
                description = description,
                phonenumber = phonenumber,
                mobilenumber = mobilenumber,
                faxnumber = faxnumber,
                email = email,
                customer = customer
            )
            contact.save()
            return HttpResponseRedirect(reverse("phonebook:contacts", args=(customer_id,)))
        else:
            return render(request, "phonebook/add_contact.html",{
                "form" : validation_form,
                "customer" : customer
            })
    return render(request, "phonebook/add_contact.html",{
                "form" : NewContactForm(),
                "customer" : customer
            })

def contact_by_id(request : HttpRequest, customer_id : int, contact_id : int):
    return render(request, "phonebook/contact.html", {
        "contact" : Contact.objects.filter(id = contact_id).first()
    })