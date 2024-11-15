from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.home, name='home'),                             # Home page
    path('apply/', views.application_form, name='application_form'),  # Multi-step application form
    path('enquiry/', views.enquiry_view, name='enquiry'),           # Enquiry form
    path('faqs/', views.faqs_view, name='faqs'),                    # FAQs
    path('complete/<int:application_id>/', views.application_complete_view, name='application_complete'),# Application complete
    # Invoice download URL
    path('download_invoice/<int:application_id>/', views.download_invoice, name='download_invoice'),


]
