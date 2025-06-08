from rest_framework import serializers
from django.conf import settings
from .models import Symptom, PredictionHistory, HealthcareFacility, MedicalHistory, UserProfile, Doctor, Consultation, Message

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_id', 'name', 'email', 'age', 'gender']
    def create(self, validate_data):
        user = UserProfile.objects.create(**validate_data)
        return user

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'


class HealthcareFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthcareFacility
        fields = '__all__'

class PredictionHistorySerializer(serializers.ModelSerializer):
    symptoms = SymptomSerializer(many=True, read_only=True)

    class Meta:
        model = PredictionHistory
        fields = '__all__'

class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_id', 'name', 'specialization', 'hospital_id']

class MessageSerializer(serializers.ModelSerializer):
    consultation = serializers.PrimaryKeyRelatedField(queryset=Consultation.objects.all())

    class Meta:
        model = Message
        fields = ['message', 'sender_id', 'sent_at', 'consultation']
