from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=100)
    vehicle_length = models.FloatField()
    vehicle_weight = models.FloatField()
    axles_number = models.IntegerField()

class Trip(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    normal_entries = models.IntegerField()
    vague_entries = models.IntegerField()
    dangerous_entries = models.IntegerField()