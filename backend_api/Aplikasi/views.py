from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Symptom, PredictionHistory, Disease
from rest_framework.views import APIView
from math import radians, sin, cos, sqrt, atan2
from .serializers import SymptomSerializer, UserRegisterSerializer, HealthcareFacility, HealthcareFacilitySerializer

class SymptomList(APIView):
    def get(self, request):
        symptoms = Symptom.objects.all().order_by('symptom_id')[:100]
        serializer = SymptomSerializer(symptoms, many=True)
        return Response(serializer.data)

class HealthcareFacilityList(APIView):
    def get(self, request):
        try:
            lat = float(request.GET.get("lat"))
            lon = float(request.GET.get("lon"))
            radius = float(request.GET.get("radius", 10))
        except (TypeError, ValueError):
            return Response({"error": "lat, lon, and radius are required and must be numbers"}, status=400)

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Earth radius in KM
            d_lat = radians(lat2 - lat1)
            d_lon = radians(lon2 - lon1)
            a = sin(d_lat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

        facilities = HealthcareFacility.objects.all()
        nearby = []

        for f in facilities:
            distance = haversine(lat, lon, float(f.latitude), float(f.longitude))
            if distance <= radius:
                f.distance = round(distance, 2)
                nearby.append(f)

        nearby.sort(key=lambda x: x.distance)

        serializer = HealthcareFacilitySerializer(nearby, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def disease_detail(request, id):
    try:
        disease = Disease.objects.get(id=id)
        return Response({
            "name": disease.name,
            "description": disease.description
        })
    except Disease.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    
@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaveDiagnosisView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        symptoms = request.data.get('symptoms')
        disease = request.data.get('disease')

        if not user_id or not isinstance(symptoms, list) or not disease:
            return Response({'error': 'user_id, symptoms (list), and disease are required.'}, status=400)
        user_id = request.data.get("user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        history = MedicalHistory.objects.create(
            user=user,
            symptoms=symptoms,
            diagnosis=disease
        )
        serializer = MedicalHistorySerializer(history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def predict_disease(request):
#     symptoms = request.data.get("symptoms", [])

#     #load model
#     # import joblib
#     # model = joblib.load("ml_model.pkl")

#     # # Create input vector here based on symptoms
#     # input_vector = convert_symptoms_to_vector(symptoms)
#     # result = model.predict([input_vector])[0]

#     # disease = Disease.objects.get(name=result)

#     # PredictionHistory.objects.create(user=request.user, disease=disease)

#     # return Response({"predicted_disease": disease.name, "description": disease.description})

#history
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def view_history(request):
#     history = PredictionHistory.objects.filter(user=request.user)
#     serializer = PredictionHistorySerializer(history, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def register_user(request):
#     serializer = UserRegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)
