from django.urls import path
from . import views

app_name = "phonebook"
urlpatterns = [
    path("", views.index, name="index"),
    path("provinces", views.provinces, name="provinces"),
    path("provinces/add", views.add_province, name="add_province"),
    path("cities", views.cities, name="cities"),
    path("cities/add", views.add_city, name="add_city"),
    path("customers",views.customers, name = "customers"),
    path("customers/add", views.add_customer, name="add_customer"),
    path("customers/<int:customer_id>", views.customer_by_id, name="customer_by_id"),
    path("customers/<int:customer_id>/contacts", views.contacts, name="contacts"),
    path("customers/<int:customer_id>/contacts/add", views.add_contact, name="add_contact"),
    path("customers/<int:customer_id>/contacts/<int:contact_id>", views.contact_by_id, name="contact_by_id"),
]
