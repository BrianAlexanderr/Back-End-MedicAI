from django.urls import path
from .views import register_user
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import SymptomList

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_piar'),
    path('api/symptoms/', SymptomList.as_view(), name='symptom-list'),
    # path('predict/', views.predict_disease),
    # path('history/', views.view_history),
    # path('disease/<int:id>/', views.disease_detail),
]