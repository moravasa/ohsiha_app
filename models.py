from django.db import models
from django.urls import reverse

# Create your models here.

class Kysymys(models.Model):
    syote = models.CharField(max_length=255)
    pvm = models.DateTimeField('julkaisupvm', auto_now_add=True)

class Juna (models.Model):
    junaTunnus = models.CharField(max_length=100)
    junaNro = models.IntegerField(null=True)
    junaAjossa = models.CharField(max_length=10, null=True)
    junaKohdeasema = models.CharField(max_length=10)
    junaLahtoasema = models.CharField(max_length=10)  
    junaLahtoaika = models.CharField(max_length=100, null=True)
    junaLahtoaikaArvio = models.CharField(max_length=100, null=True)
    junaLahtoaikaTod = models.CharField(max_length=100, null=True)
    junaMyohassa = models.CharField(max_length=10, null=True)
    junaMyohassaMin = models.IntegerField(null=True)
    junaPeruttu = models.CharField(max_length=10, null=True)

class Asetukset (models.Model):
    SettingName = models.CharField(max_length=100)
    SettingValue = models.CharField(max_length=100, null=True)
    SettingUser = models.CharField(max_length=100, null=True)
    Modified = models.DateTimeField(auto_now_add=True, null=True)
    

class JunaSijainti (models.Model):
    junaNro = models.IntegerField()
    junaTunnus = models.CharField(max_length=100, null=True)
    junaLahtoaika = models.CharField(max_length=100)
    junaTimeStamp = models.CharField(max_length=100)
    junaKoordLat = models.CharField(max_length=100, null=True)
    junaKoordLong = models.CharField(max_length=100, null=True)
    junaNopeus = models.CharField(max_length=20, null=True)