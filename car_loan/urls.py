"""
URL configuration for car_loan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include  # Import include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from applications.views import ApplicationViewSet, PersonalDetailsViewSet, LoanDetailsViewSet, DocumentUploadViewSet  # Adjust import based on your app structure

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'applications', ApplicationViewSet)
router.register(r'personal_details', PersonalDetailsViewSet)
router.register(r'loan_details', LoanDetailsViewSet)
router.register(r'documents', DocumentUploadViewSet)

# The URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel URL
    path('api/', include(router.urls)),  # Include the router URLs under 'api/' prefix
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files during development
