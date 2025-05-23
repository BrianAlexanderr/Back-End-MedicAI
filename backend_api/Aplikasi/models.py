from django.db import models
from django.contrib.auth.models import User

class Symptom(models.Model):
    symptom_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'symptoms'
    managed = False

class HealthcareFacility(models.Model):
    facility_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    photo = models.BinaryField() 

    class Meta:
        db_table = 'healthcarefacilities'
        managed = False 
class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
