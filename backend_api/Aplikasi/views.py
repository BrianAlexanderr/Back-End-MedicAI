from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .models import Symptom, PredictionHistory, Disease, UserProfile, MedicalHistory, Doctor, DoctorSpeciality, Consultation, Message
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import OuterRef, Subquery, F
from .serializers import SymptomSerializer, UserRegisterSerializer, HealthcareFacility, HealthcareFacilitySerializer, MedicalHistorySerializer, PredictionHistorySerializer, DoctorSerializer, MessageSerializer
import json
from django.http import JsonResponse, HttpResponse
import os
import pickle
import numpy as np
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
LabelEncoderPath = os.path.join(os.path.dirname(__file__), "label_encoder.pkl")

with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)

with open(LabelEncoderPath, 'rb') as label_file:
    le = pickle.load(label_file)

# Example: Define symptom columns (Replace this with actual features used in your model)
SYMPTOM_COLUMNS = [
    "Gatal", "Ruam kulit", "Erupsi kulit nodular", "Bersin terus-menerus", "Menggigil",
    "Kedinginan", "Nyeri sendi", "Asam lambung", "Sariawan di lidah", "Penyusutan otot",
    "Muntah", "Sensasi terbakar saat buang air kecil", "Bercak saat buang air kecil", "Kelelahan",
    "Kenaikan berat badan", "Kecemasan", "Tangan dan kaki dingin", "Perubahan suasana hati",
    "Penurunan berat badan", "Gelisah", "Lesu", "Bercak di tenggorokan", "Kadar gula darah tidak teratur",
    "Batuk", "Demam tinggi", "Mata cekung", "Sesak napas", "Berkeringat", "Dehidrasi",
    "Gangguan pencernaan", "Sakit kepala", "Kulit menguning", "Urin gelap", "Mual",
    "Kehilangan nafsu makan", "Nyeri di belakang mata", "Sakit punggung", "Sembelit",
    "Nyeri perut", "Diare", "Demam ringan", "Urin kuning", "Mata menguning", "Gagal hati akut",
    "Kelebihan cairan dalam tubuh", "Perut membengkak", "Pembengkakan kelenjar getah bening",
    "Rasa tidak enak badan", "Penglihatan kabur dan terdistorsi", "Dahak", "Iritasi tenggorokan",
    "Mata merah", "Tekanan sinus", "Hidung berair", "Hidung tersumbat", "Nyeri dada",
    "Kelemahan pada anggota tubuh", "Detak jantung cepat", "Nyeri saat buang air besar",
    "Nyeri di daerah anus", "Tinja berdarah", "Iritasi di anus", "Nyeri leher", "Pusing",
    "Kram", "Mudah memar", "Obesitas", "Kaki bengkak", "Pembuluh darah bengkak",
    "Wajah dan mata bengkak", "Pembesaran kelenjar tiroid", "Kuku rapuh", "Pembengkakan ekstremitas",
    "Rasa lapar berlebihan", "Kontak seksual di luar nikah", "Bibir kering dan kesemutan",
    "Bicara cadel", "Nyeri lutut", "Nyeri sendi pinggul", "Kelemahan otot", "Leher kaku",
    "Pembengkakan sendi", "Kekakuan gerakan", "Sensasi berputar", "Kehilangan keseimbangan",
    "Ketidakstabilan saat berjalan", "Kelemahan pada satu sisi tubuh", "Kehilangan indera penciuman",
    "Ketidaknyamanan kandung kemih", "Bau urin yang menyengat", "Perasaan ingin buang air kecil terus-menerus",
    "Sering buang angin", "Gatal di dalam tubuh", "Tampilan toksik (typhos)", "Depresi",
    "Mudah marah", "Nyeri otot", "Gangguan sensorik", "Bintik merah di seluruh tubuh",
    "Sakit perut", "Menstruasi tidak normal", "Bercak warna tidak normal pada kulit",
    "Mata berair", "Nafsu makan meningkat", "Sering buang air kecil", "Riwayat keluarga",
    "Dahak berlendir", "Dahak berwarna karat", "Kurang konsentrasi", "Gangguan penglihatan",
    "Menerima transfusi darah", "Menerima suntikan tidak steril", "Koma", "Pendarahan lambung",
    "Perut kembung", "Riwayat konsumsi alkohol", "Kelebihan cairan tubuh", "Darah dalam dahak",
    "Pembuluh darah menonjol di betis", "Jantung berdebar", "Nyeri saat berjalan",
    "Jerawat bernanah", "Komedo", "Kulit bersisik", "Kulit mengelupas", "Serpihan seperti perak pada kulit",
    "Lekukan kecil pada kuku", "Kuku meradang", "Lepuhan", "Luka merah di sekitar hidung",
    "Kerak kuning yang keluar dari kulit"
]


class SymptomList(APIView):
    def get(self, request):
        symptoms = Symptom.objects.all().order_by('name')
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
            R = 6371
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
    
def get_photo(request, facility_id):
    hospitals = hospitals.objects.get(facility_id=facility_id)
    if hospitals.photo:
        return HttpResponse(hospitals.photo, content_type="image/jpeg")  # Adjust if PNG
    return HttpResponse(status=404)
    

@api_view(['POST'])
def get_precautions(request):
    try:
        # Parse JSON request
        data = json.loads(request.body.decode("utf-8"))
        predicted_disease = data.get("disease", "").strip()

        # Retrieve the disease from the database
        disease = Disease.objects.filter(name__iexact=predicted_disease).first()

        return JsonResponse({
            "disease": disease.name,
            "precautions": disease.precautions
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
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
        diagnosis = request.data.get('diagnosis')
        doctor_notes = request.data.get('doctor_notes', '')
        symptoms = request.data.get('symptoms', [])

        if not user_id or not diagnosis:
            return Response({'error': 'Missing data'}, status=400)

        history = MedicalHistory.objects.create(
            user_id=user_id,
            diagnosis=diagnosis,
            doctor_notes=doctor_notes,
            symptoms=symptoms
        )

        return Response({'message': 'Diagnosis history saved successfully'}, status=201)

@api_view(['POST'])
def get_symptom_names(request):
    if request.method == "POST":
        data = json.loads(request.body)
        symptom_ids = data.get("symptom_ids", [])
        symptoms = Symptom.objects.filter(symptom_id__in=symptom_ids).values("symptom_id", "name")
        return JsonResponse({"symptoms": list(symptoms)}, safe=False)

@csrf_exempt
@api_view(['POST'])
def predict_disease(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            symptom_ids = data.get("symptoms", [])

            if not symptom_ids:
                return JsonResponse({"error": "No symptoms provided"}, status=400)

            # Fetch symptom names
            symptom_names = list(Symptom.objects.filter(symptom_id__in=symptom_ids).values_list("name", flat=True))

            # Check if all IDs were found
            if len(symptom_names) != len(symptom_ids):
                missing_ids = set(symptom_ids) - set(Symptom.objects.values_list("id", flat=True))
                print(f"⚠️ Warning: Some symptom IDs not found in the database: {missing_ids}")
                return JsonResponse({"error": f"Symptom IDs not found: {missing_ids}"}, status=400)

            # Convert symptoms into a DataFrame
            symptom_vector = pd.DataFrame([np.zeros(len(SYMPTOM_COLUMNS))], columns=SYMPTOM_COLUMNS)

            # Mark selected symptoms as 1
            for symptom in symptom_names:
                if symptom in SYMPTOM_COLUMNS:
                    symptom_vector[symptom] = 1
                else:
                    print(f"⚠️ Warning: Symptom '{symptom}' not found in SYMPTOM_COLUMNS")
            
            # Predict disease
            y_proba = model.predict_proba(symptom_vector)  # Get probabilities
            predicted_index = np.argmax(y_proba, axis=1)[0]  # Get highest probability index
            predicted_disease = le.inverse_transform(np.array([predicted_index]))[0]  # Convert index to disease name
            confidence_score = round(float(y_proba[0][predicted_index]), 2)  # Get confidence score
            
            try:
                disease = Disease.objects.get(name=predicted_disease)
                disease_id = disease.disease_id  # Ensure this matches your model's column name
            except Disease.DoesNotExist:
                print(f"⚠️ Warning: Predicted disease '{predicted_disease}' not found in database")
                return JsonResponse({"error": f"Disease '{predicted_disease}' not found in database"}, status=404)
            
            return JsonResponse({
                "disease_id" : disease_id,
                "disease": predicted_disease,
                "confidence_score": round(confidence_score, 1)  # Round for readability
            })

        except Exception as e:
            print("❌ Exception occurred:", str(e))  # Debugging
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

@api_view(['GET'])
def view_history(request, user_id):
    history = MedicalHistory.objects.filter(user=user_id).order_by('-created_at')
    serializer = MedicalHistorySerializer(history, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_recommended_doctors(request, disease_id):
    try:
        # Find the disease object
        disease = Disease.objects.get(disease_id=disease_id)  # Use `disease_id` from your SQL error

        # Find doctor IDs that are linked to this disease
        doctor_ids = DoctorSpeciality.objects.filter(disease=disease).values_list('doctor_id', flat=True)

        # Retrieve doctor details
        doctors = Doctor.objects.filter(doctor_id__in=doctor_ids)

        # Serialize the doctor data
        serializer = DoctorSerializer(doctors, many=True)
        return Response({"doctors": serializer.data}, status=status.HTTP_200_OK)

    except Disease.DoesNotExist:
        return Response({"error": "Disease not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        consultation_id = self.kwargs['consultation_id']
        return Message.objects.filter(consultation_id=consultation_id).order_by('sent_at')
    
class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        consultation_id = self.request.data.get('consultation')
        consultation = Consultation.objects.get(id=consultation_id)
        sender_id = self.request.data.get('sender_id')
        sender = None
        if sender_id:
            try:
                sender = UserProfile.objects.get(user_id=sender_id)
            except UserProfile.DoesNotExist:
                print("UserProfile tidak ditemukan")
        serializer.save(
            sender=sender,  # if you're using UserProfile
            consultation=consultation
        )

class GetOrCreateConsultationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        user_id = request.data.get('user_id')
        doctor_id = request.data.get('doctor_id')
        if not doctor_id:
            return Response({'error': 'doctor_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = Doctor.objects.get(doctor_id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Ambil UserProfile berdasarkan user login (yang pakai Firebase UID)
            user_profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

        # Cari atau buat konsultasi baru
        consultation, created = Consultation.objects.get_or_create(
            user_id=user_profile.user_id,
            doctor=doctor
        )

        data = {
            'consultation_id': consultation.id,
            'created': created
        }
        
        json_string = json.dumps(data, ensure_ascii=False)

        return Response(json.loads(json_string))

def get_chat_list_for_patient(patient_id):
    # Get consultations for this patient
    consultations = Consultation.objects.filter(user_id=patient_id)

    # Subquery to get latest message per consultation
    latest_message_subquery = Message.objects.filter(
        consultation_id=OuterRef('pk')
    ).order_by('-sent_at')

    consultations = consultations.annotate(
        doctor_name=F('doctor__name'),
        doctor_speciality=F('doctor__specialization'), 
        last_message=Subquery(latest_message_subquery.values('message')[:1]),
        last_message_time=Subquery(latest_message_subquery.values('sent_at')[:1]),
    ).order_by('-last_message_time')

    # Format the result for the API response
    chat_list = []
    for c in consultations:
        chat_list.append({
            'consultation_id': c.id,
            'doctor_id': c.doctor_id,
            'doctor_name': c.doctor_name,
            'doctor_speciality': c.doctor_speciality,
            'last_message': c.last_message or "",
            'last_message_time': c.last_message_time,
        })

    return chat_list

class PatientChatListAPIView(APIView):
    def get(self, request, patient_id):
        chats = get_chat_list_for_patient(patient_id)
        return Response(chats)

@api_view(['GET'])
def get_hospitals(request):
    hospitals = HealthcareFacility.objects.all()
    serializer = HealthcareFacilitySerializer(hospitals, many=True)
    return Response(serializer.data)

def get_photo(request, facility_id):
    hospitals = hospitals.objects.get(facility_id=facility_id)
    if hospitals.photo:
        return HttpResponse(hospitals.photo, content_type="image/jpeg")  # Adjust if PNG
    return HttpResponse(status=404)