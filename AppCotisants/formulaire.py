from django import forms
from django.forms import ModelForm
from django.utils import timezone
from .models import Cotisants, Produits, Vente

class CotisantForm(ModelForm):
    class Meta:
        model = Cotisants
        fields = ['prenom', 'nom','mail','temps_cotisation','solde']

class ProduitForm(ModelForm):
    class Meta:
        model = Produits
        fields = ['nom', 'prix']



