"""
URL configuration for backend_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from backend_api.Aplikasi.views import register_user, SymptomList, HealthcareFacilityList, SaveDiagnosisView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend_api.Aplikasi.urls')), 
    path('register/', register_user),
    path('symptoms/', SymptomList.as_view()),
    path('facilities/', HealthcareFacilityList.as_view(), name='facility-list'),
    path('save-diagnosis/', SaveDiagnosisView.as_view(), name='save-diagnosis'),
]