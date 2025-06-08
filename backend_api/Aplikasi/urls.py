from django.urls import path
from .views import register_user, get_precautions, get_symptom_names, get_recommended_doctors, get_hospitals, get_photo
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import SymptomList, SaveDiagnosisView, HealthcareFacilityList, MessageListView, GetOrCreateConsultationView, PatientChatListAPIView, SendMessageView

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_piar'),
    path('symptoms/', SymptomList.as_view(), name='symptom-list'),
    path('get_precautions/', get_precautions, name='get_precautions'),
    path('save_diagnosis/', SaveDiagnosisView.as_view(), name='save_history'),
    path('predict/', views.predict_disease),
    path('get_symptom_names/', get_symptom_names),
    path('doctors/<int:disease_id>/', get_recommended_doctors),
    path('facilities/', HealthcareFacilityList.as_view()),
    path('history/<str:user_id>/', views.view_history),
    path('consultations/<int:consultation_id>/messages/', MessageListView.as_view(), name='view-messages'),
    path('messages/send/', SendMessageView.as_view(), name='send-message'),
    path('consultations/get_or_create/', GetOrCreateConsultationView.as_view(), name='get_or_create_consultation'),
    path('patients/<str:patient_id>/chats/', PatientChatListAPIView.as_view(), name='patient-chats'),
    path('nearby_facilities/', get_hospitals, name='get_facilities'),
    path('nearby_facilities/photo/<int:facility_id>/', get_photo, name='get_facility_photo'),
]