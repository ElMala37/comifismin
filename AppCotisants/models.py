from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.db import models
from django.shortcuts import redirect
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.contrib import admin
# Create your models here.



class Cotisants(models.Model):
    prenom = models.CharField(max_length=15)
    nom = models.CharField(max_length=15)
    nomprenom = models.CharField(max_length=30, unique=True, default='')
    solde = models.DecimalField(max_digits=8, decimal_places=2, default='0')
    date_inscription = models.DateTimeField(auto_now_add=True)
    depense = models.DecimalField(max_digits=8, decimal_places=2, default='0')
    mail = models.EmailField(max_length=40, default='')
    promo = models.CharField(max_length=40, default='')
    DUREE_CHOICES = (
        (timedelta(days=365), '1 an'),
        (timedelta(days=183), '6 mois'),
        (timedelta(days=6), '6 jours'),
    )
    temps_cotisation = models.DurationField(choices=DUREE_CHOICES, default=None)
    date_fin = models.DateField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.nomprenom:
            self.nomprenom = unidecode(f"{self.nom}{self.prenom}").upper()
        if self.temps_cotisation:
            self.date_fin = timezone.now().date() + self.temps_cotisation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class CatProduit(models.Model):
    categorie = models.CharField(max_length=50)

class Produits(models.Model):
    nom = models.CharField(max_length=30, unique=True)
    type_produit = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.nom}"



class Vente(models.Model):

    client_id = models.ForeignKey(Cotisants, on_delete=models.CASCADE, default=1)
    produit_id = models.ForeignKey(Produits, on_delete=models.CASCADE, default=1)
    client = models.CharField(max_length=50)
    produit = models.CharField(max_length=50, default='')
    compte_serveur = models.CharField(max_length=30)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Encaissement(models.Model):
    client_id = models.ForeignKey(Cotisants, on_delete=models.CASCADE, default=1)
    client = models.CharField(max_length=50)
    montant = models.DecimalField(max_digits=8, decimal_places=2)
    mode_paiement = models.CharField(max_length=50,default='')
    compte_serveur = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)

class AjoutStock(models.Model):
    produit_id = models.ForeignKey(Produits, on_delete=models.CASCADE, default=1)
    produit = models.CharField(max_length=50, default='')
    quantity = models.IntegerField(default=0)
    nouv_prix = models.DecimalField(max_digits=8, decimal_places=2, default='0')
    ancien_prix = models.DecimalField(max_digits=8, decimal_places=2, default='0')
    compte_serveur = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)

class Connexion(models.Model):
    compte_serveur = models.CharField(max_length=30)
    date_connexion = models.DateTimeField(auto_now_add=True)

class SupVente(models.Model):
    produit = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    client = models.CharField(max_length=50)
    compte_serveur = models.CharField(max_length=30)
    date_suppression = models.DateTimeField(auto_now_add=True)

class SupCot(models.Model):
    client = models.CharField(max_length=50)
    compte_serveur = models.CharField(max_length=30)
    date_suppression = models.DateTimeField(auto_now_add=True)

class FavorisTibbar(models.Model):
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE, default=1, related_name='favoris_tibbar')
class FavorisTipause(models.Model):
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE, default=1,  related_name='favoris_tipause')

class DatesStat(models.Model):
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()



class Promo(models.Model):
    promo = models.CharField(max_length=50)

class ModePaiement(models.Model):
    mode = models.CharField(max_length=50)