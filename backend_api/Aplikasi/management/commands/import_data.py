import csv
from django.core.management.base import BaseCommand
from Aplikasi.models import Disease, Symptom, DiseaseSymptom

class Command(BaseCommand):
    help = 'Import diseases, symptoms, and disease-symptoms mappings from CSV files'

    def handle(self, *args, **kwargs):
        with open('diseases.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                name = row[0].strip()
                Disease.objects.get_or_create(name=name)
        with open('symptoms.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                name = row[0].strip()
                Symptom.objects.get_or_create(name=name)
        with open('disease_symptoms.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                disease_name = row[0].strip()
                symptom_name = row[1].strip()

                try:
                    disease = Disease.objects.get(name=disease_name)
                    symptom = Symptom.objects.get(name=symptom_name)
                    DiseaseSymptom.objects.get_or_create(disease=disease, symptom=symptom)
                except Disease.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Disease '{disease_name}' not found"))
                except Symptom.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Symptom '{symptom_name}' not found"))
        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))