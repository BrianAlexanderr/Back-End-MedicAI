from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from .models import Symptom, PredictionHistory, HealthcareFacility

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password do not match.")
        return data
    def create(self, validate_data):
        validate_data.pop('confirm_password')
        user = User.objects.create_user(**validate_data)
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
        fields = [
            'id',
            'symptoms',
            'predicted_disease',
            'explanation',
            'created_at',
        ]

class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '_all_'