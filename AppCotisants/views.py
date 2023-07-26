from django.contrib.auth import get_user, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Cotisants, Produits, Vente, Encaissement, AjoutStock, Connexion, SupVente, FavorisTipause, \
    FavorisTibbar, DatesStat, CatProduit, ModePaiement, Promo, SupCot
from .formulaire import CotisantForm, ProduitForm
from datetime import timedelta, datetime, date
from django.utils import timezone
from django.db import IntegrityError
from decimal import Decimal
from django.contrib import messages
from collections import Counter
from django.db.models import Count, Sum
from django.core.management import call_command



@login_required
def welcome(request):
    context = {
        'username': request.user.username
    }
    return render(request, 'index.html', context)

@login_required
def index(request):
    if request.method == "POST":
        form = CotisantForm(request.POST)
        promo = request.POST.get('options2')
        mode = request.POST.get('options1')
        print("promo",promo)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.promo = promo
                instance.save()
                client_id = instance.pk  # Récupère l'ID de l'instance
                cotisant = get_object_or_404(Cotisants, id=client_id)
                encaissement = Encaissement(
                    client_id=cotisant,
                    client=f"{cotisant.prenom} {cotisant.nom}",
                    montant=cotisant.solde,
                    mode_paiement=mode,
                    compte_serveur=request.user.username, )
                encaissement.save()
                return redirect('/ajtcotisants')
            except IntegrityError:
                form.add_error('nom', 'Un cotisant avec ce nom et prénom existe déjà.')
    else:
        form = CotisantForm()
    return render(request, 'ajtcotisants2.html', {'dataMode':ModePaiement.objects.all(),'dataPromo':Promo.objects.all(),'form': form, 'dataCotisants': Cotisants.objects.order_by('nom').all(),'username': request.user.username})

@login_required
def index2(request):
    return render(request, 'gstsoldes.html',{'dataMode':ModePaiement.objects.all(),'dataCotisants':Cotisants.objects.order_by('date_inscription').all(),'username': request.user.username})

@login_required
def mod_cst(request):
    return render(request, 'gstcotisants.html',{'dataCotisants':Cotisants.objects.order_by('date_inscription').all(),'username': request.user.username})



@login_required
def index3(request):
    return render(request, 'supcotisants.html',{'dataCotisants':Cotisants.objects.order_by('date_fin').all(),'username': request.user.username})

@login_required
def update_solde(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Vérifier les informations d'identification de l'utilisateur
        user = authenticate(username=username, password=password)
        if user is None:
            # Informations d'identification invalides, rediriger vers une page d'erreur ou afficher un message d'erreur
            return render(request, 'gstsoldes.html', {'erreur_auth': True, 'dataMode':ModePaiement.objects.all(),'dataCotisants':Cotisants.objects.order_by('date_inscription').all(),'username': request.user.username})
        cotisant_id = request.POST.get('id_modified')
        solde_to_add = Decimal(request.POST.get('soldeToAdd'))
        mode = request.POST.get('options')
        cotisant = get_object_or_404(Cotisants, id=cotisant_id)
        print(f"{cotisant.prenom}{cotisant.nom}".lower())
        if f"{cotisant.prenom}{cotisant.nom}".lower()==username:
            return render(request, 'gstsoldes.html',
                          {'erreur_auth': True, 'dataMode': ModePaiement.objects.all(),
                           'dataCotisants': Cotisants.objects.order_by('date_inscription').all(),
                           'username': request.user.username})
        cotisant.solde += solde_to_add
        encaissement = Encaissement(
            client_id=cotisant,
            client=f"{cotisant.prenom} {cotisant.nom}",
            mode_paiement=mode,
            montant=solde_to_add,
            compte_serveur=username,)
        encaissement.save()
        cotisant.save()
        return HttpResponseRedirect('/gstsoldes')  # Remplacez par l'URL de redirection souhaitée
    return redirect('/gstsoldes')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def update_duree(request):
    if request.method == 'POST':
        cotisants_ids = request.POST.get('cotisants_ids')
        duree = request.POST.get('selectOption')
        print(duree)
        print("cotisants : ",cotisants_ids)
        if cotisants_ids.endswith(','):
            cotisants_ids = cotisants_ids[:-1]
        elements = cotisants_ids.split(',')
        listeCID = []
        for element in elements:
            if element:
                listeCID.append(int(element))
        for i in listeCID:
            cotisant = Cotisants.objects.get(id=i)
            cotisant.date_inscription = timezone.now().date()
            if duree == "1 an":
                cotisant.temps_cotisation = timedelta(days=365)
            elif duree == "6 mois":
                cotisant.temps_cotisation = timedelta(days=183)
            elif duree == "6 jours":
                cotisant.temps_cotisation = timedelta(days=6)
            cotisant.date_fin = timezone.now().date() + cotisant.temps_cotisation
            cotisant.save()
        return HttpResponseRedirect('/gstcotisants')  # Remplacez par l'URL de redirection souhaitée
    return redirect('/gstcotisants')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def delete_cotisant(request):
    if request.method == 'POST':
        cotisant_id = request.POST.get('id_modified')
        cotisant = get_object_or_404(Cotisants, id=cotisant_id)
        supcot = SupCot(
            client=f"{cotisant.prenom} {cotisant.nom}",
            compte_serveur=request.user.username
        )
        supcot.save()
        cotisant.delete()
        return HttpResponseRedirect('/supcotisants')  # Remplacez par l'URL de redirection souhaitée
    return redirect('/supcotisants')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def voirsupcot(request):
    return render(request, 'voirsupcot.html',{'dataSupCot':SupCot.objects.order_by('-date_suppression').all(),'username': request.user.username})


@login_required
def ajtproduits(request):
    if request.method == "POST":
        form = ProduitForm(request.POST)
        type = request.POST.get('options')
        print("type",type)
        if form.is_valid():
            try:
                produit = form.save(commit=False)
                produit.type_produit = type
                produit.save()
                return redirect('/ajtproduits')
            except IntegrityError:
                form.add_error('nom', 'Un produit avec ce nom existe déjà.')
    else:
        form = ProduitForm()
    return render(request, 'ajtproduit.html', {'dataType':CatProduit.objects.all(),'form': form, 'dataProduits': Produits.objects.order_by('nom').all(),'username': request.user.username})

@login_required
def index4(request):
    return render(request, 'gstproduits.html',{'dataProduits':Produits.objects.order_by('nom').all(),'dataFavorisTipause':FavorisTipause.objects.all(), 'dataFavorisTibbar':FavorisTibbar.objects.all(),'username': request.user.username})

@login_required
def update_stock(request):
    if request.method == 'POST':
        produit_id = request.POST.get('id_modified')
        old_price = request.POST.get('old_price')
        old_price = old_price.replace(',', '.')
        print('old_price',old_price)
        quantity_to_add = int(request.POST.get('quantityToAdd',0))
        new_price = Decimal(request.POST.get('NewPrice'))
        produit = get_object_or_404(Produits, id=produit_id)
        produit.quantity += quantity_to_add
        produit.prix = new_price
        ajout = AjoutStock(
            produit_id=produit,
            produit=f"{produit.nom}",
            ancien_prix=old_price,
            nouv_prix=new_price,
            quantity=quantity_to_add,
            compte_serveur=request.user.username, )
        print("Creating vente...")
        ajout.save()
        produit.save()
        return HttpResponseRedirect('/gstproduits')  # Remplacez par l'URL de redirection souhaité
    return redirect('/gstproduits')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def ajt_favoris_tb(request):
    if request.method == 'POST':
        produit_id = request.POST.get('id_modified2')
        produitfav = get_object_or_404(Produits, id=produit_id)
        choix = request.POST.get('favoris')
        if choix=="Oui":
            fav=FavorisTibbar(produit = produitfav)
            try:
                fav.save()
            except IntegrityError:
                messages.error(request, "Ce produit est déjà dans les favoris du Tibbar")#ne fera rien car j'ai pas configurer les message dans le setting
        return HttpResponseRedirect('/gstfavoris')  # Remplacez par l'URL de redirection souhaité
    return redirect('/gstfavoris')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def del_favoris_tb(request):
    if request.method == 'POST':
        favtb_id = request.POST.get('id_modified3')
        choix = request.POST.get('favoris')
        if choix=="Oui":
            favori = get_object_or_404(FavorisTibbar, id=favtb_id)
            favori.delete()
        return HttpResponseRedirect('/gstfavoris')  # Remplacez par l'URL de redirection souhaité
    return redirect('/gstfavoris')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def ajt_favoris_tp(request):
    if request.method == 'POST':
        produit_id = request.POST.get('id_modified4')
        produitfav = get_object_or_404(Produits, id=produit_id)
        choix = request.POST.get('favoris')
        if choix=="Oui":
            fav=FavorisTipause(produit = produitfav)
            try:
                fav.save()
            except IntegrityError:
                messages.error(request, "Ce produit est déjà dans les favoris du Tipause")#ne fera rien car j'ai pas configurer les message dans le setting
        return HttpResponseRedirect('/gstfavoris')  # Remplacez par l'URL de redirection souhaité
    return redirect('/gstfavoris')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def del_favoris_tp(request):
    if request.method == 'POST':
        favtp_id = request.POST.get('id_modified5')
        choix = request.POST.get('favoris')
        if choix=="Oui":
            favori = get_object_or_404(FavorisTipause, id=favtp_id)
            favori.delete()
        return HttpResponseRedirect('/gstfavoris')  # Remplacez par l'URL de redirection souhaité
    return redirect('/gstfavoris')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def gstfavoris(request):
    return render(request, 'gstfavoris.html',{'dataProduits':Produits.objects.order_by('nom').all(),'dataFavorisTipause':FavorisTipause.objects.all(), 'dataFavorisTibbar':FavorisTibbar.objects.all(),'username': request.user.username})


@login_required
def index5(request):
    return render(request, 'supproduits.html',{'dataProduits':Produits.objects.order_by('nom').all(),'username': request.user.username})

@login_required
def type_produits(request):
    return render(request, 'typeproduits.html',{'dataType':CatProduit.objects.all(),'username': request.user.username})

@login_required
def ajt_type(request):
    if request.method == 'POST':
        categorie = request.POST.get('texte')
        Type = CatProduit(categorie=categorie)
        Type.save()
        return HttpResponseRedirect('/type_produits')  # Remplacez par l'URL de redirection souhaitée
    return redirect('/type_produits')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def del_type(request):
    if request.method == 'POST':
        type_id = request.POST.get('id_modified')
        Type = get_object_or_404(CatProduit, id=type_id)
        Type.delete()
        return HttpResponseRedirect('/type_produits')  # Remplacez par l'URL de redirection souhaitée
    return redirect('/type_produits')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST


@login_required
def delete_produit(request):
    if request.method == 'POST':
        produit_id = request.POST.get('id_modified')
        produit = get_object_or_404(Produits, id=produit_id)
        produit.delete()
        return HttpResponseRedirect('/supproduits')  # Remplacez par l'URL de redirection souhaitée
    return redirect('/supproduits')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def ajouter_vente(request):
    now = date.today()
    print(now)
    return render(request, 'ajtvente3.html',{'now':now,'dataProduits':Produits.objects.all(), 'dataCotisants':Cotisants.objects.order_by('nom').all(),'username': request.user.username, 'dataFavorisTB':FavorisTibbar.objects.all(),'dataFavorisTP':FavorisTipause.objects.all()})


@login_required
def final_vente(request):
    if request.method == 'POST':
        clientId = request.POST.get('id_client')
        chaineId = request.POST.get('produits_ids')
        print("clientId:", clientId)
        print("chaineId:", chaineId)
        if clientId:
            if chaineId.endswith(','):
                chaineId = chaineId[:-1]
            elements = chaineId.split(',')
            listeProduitId = []
            for element in elements:
                if element:
                    listeProduitId.append(int(element))
            for i in listeProduitId:
                client = Cotisants.objects.get(id=clientId)
                produit = Produits.objects.get(id=i)
                client.solde -= produit.prix
                client.depense += produit.prix
                produit.quantity -= 1
                print("client:", client)
                print("produit:", produit)
                vente = Vente(
                client_id=client,
                produit_id=produit,
                client=f"{client.prenom} {client.nom}",
                produit=produit.nom,
                compte_serveur= request.user.username,
                prix=produit.prix)
                print("Creating vente...")
                vente.save()
                client.save()
                produit.save()
            return HttpResponseRedirect('/ajtvente')  # Remplacez par l'URL de redirection souhaité
    return redirect('/ajtvente')

@login_required
def voir_ventes(request):
    return render(request, 'voirventes2.html',{'dataVentes':Vente.objects.order_by('-date').all(),'username': request.user.username})

@login_required
def delete_vente(request):
    if request.method == 'POST':
        vente_id = request.POST.get('id_modified')
        vente = get_object_or_404(Vente, id=vente_id)
        client = get_object_or_404(Cotisants, id=vente.client_id.id)
        produit = get_object_or_404(Produits, id=vente.produit_id.id)
        client.solde += vente.prix
        produit.quantity += 1
        delvente = SupVente(
            produit = produit.nom,
            prix = produit.prix,
            client =f"{client.prenom} {client.nom}",
            compte_serveur = request.user.username)
        delvente.save()
        client.save()
        produit.save()
        vente.delete()
        return HttpResponseRedirect('/voirventes')  # Remplacez par l'URL de redirection souhaitée
    return redirect('/voirventes')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def voir_encaissement(request):
    return render(request, 'voirencaissements.html',{'dataEncaissements':Encaissement.objects.order_by('-date').all(),'username': request.user.username})

@login_required
def type_paiements(request):
    return render(request, 'typepaiements.html',{'dataMode':ModePaiement.objects.all(),'username': request.user.username})

@login_required
def ajt_modep(request):
    if request.method == 'POST':
        mode = request.POST.get('texte')
        Type = ModePaiement(mode=mode)
        Type.save()
        return HttpResponseRedirect('/type_paiements')  # Remplacez par l'URL de redirection souhaitée
    return redirect('/type_paiements')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def del_modep(request):
    if request.method == 'POST':
        type_id = request.POST.get('id_modified')
        Type = get_object_or_404(ModePaiement, id=type_id)
        Type.delete()
        return HttpResponseRedirect('/type_paiements')  # Remplacez par l'URL de redirection souhaitée
    return redirect('/type_paiements')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def promo(request):
    return render(request, 'promo.html',{'dataPromo':Promo.objects.all(),'username': request.user.username})

@login_required
def ajt_promo(request):
    if request.method == 'POST':
        promo = request.POST.get('texte')
        Type = Promo(promo=promo)
        Type.save()
        return HttpResponseRedirect('/promo')  # Remplacez par l'URL de redirection souhaitée
    return redirect('/promo')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def del_promo(request):
    if request.method == 'POST':
        type_id = request.POST.get('id_modified')
        Type = get_object_or_404(Promo, id=type_id)
        Type.delete()
        return HttpResponseRedirect('/promo')  # Remplacez par l'URL de redirection souhaitée
    return redirect('/promo')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def voir_ajoutstock(request):
    return render(request, 'voirajtproduits.html',{'dataAjoutStock':AjoutStock.objects.order_by('-date').all(),'username': request.user.username})

@login_required
def voir_cnx(request):
    return render(request, 'voirconnexions.html',{'dataConnexions':Connexion.objects.order_by('-date_connexion').all(),'username': request.user.username})

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Appel de la méthode form_valid de la classe parente
        super().form_valid(form)
        # Récupérer l'utilisateur connecté
        user = self.request.user
        # Créer et enregistrer l'objet avec les données souhaitées
        cnx = Connexion(compte_serveur=user)
        cnx.save()
        return redirect('/welcome')  # Rediriger vers la page d'accueil après l'enregistrement de l'objet

@login_required
def voir_supvente(request):
    return render(request, 'voirsupvente.html',{'dataSupVentes':SupVente.objects.order_by('-date_suppression').all(),'username': request.user.username})


@login_required
def tresorerie(request):
    # Récupérer les cotisants avec un solde positif
    cotisants_positifs = Cotisants.objects.filter(solde__gt=0)
    # Récupérer les cotisants avec un solde négatif
    cotisants_negatifs = Cotisants.objects.filter(solde__lt=0)
    # Calculer la somme des soldes positifs
    somme_soldes_positifs = cotisants_positifs.aggregate(somme_soldes=Sum('solde'))['somme_soldes']
    # Calculer la somme des soldes négatifs
    somme_soldes_negatifs = cotisants_negatifs.aggregate(somme_soldes=Sum('solde'))['somme_soldes']
    if not DatesStat.objects.exists():
        date_debut = datetime.strptime('2023-05-26', '%Y-%m-%d')
        date_fin = datetime.now().date() + timedelta(days=1)
        date_stat = DatesStat(date_debut=date_debut, date_fin=date_fin)
        date_stat.save()
    date_stat = DatesStat.objects.first()  # Récupérer le premier objet DatesStat
    date_debut = date_stat.date_debut
    date_fin = date_stat.date_fin
    encaissement=Encaissement.objects.filter(date__range=(date_debut, date_fin))
    # Récupérer le total des montants des encaissements
    total_encaissements = encaissement.aggregate(total_montant=Sum('montant'))['total_montant']
    # Récupérer toutes les ventes comprises entre les dates spécifiées
    ventes = Vente.objects.filter(date__range=(date_debut, date_fin))
    # Créer un dictionnaire pour stocker les produits achetés par chaque utilisateur
    produits_par_client = {}
    # Boucler sur chaque vente
    for vente in ventes:
        client = vente.client  # Remplacez "utilisateur" par le nom du champ représentant l'utilisateur dans le modèle Vente
        produit = vente.produit  # Remplacez "produit" par le nom du champ représentant le produit dans le modèle Vente
        if client not in produits_par_client:
            produits_par_client[client] = Counter()
        # Incrémenter le compteur pour ce produit acheté par cet utilisateur
        produits_par_client[client][produit] += 1
    # Tri décroissant des produits achetés pour chaque utilisateur
    produits_par_client_tries = {
        client: produits.most_common() for client, produits in produits_par_client.items()
    }
    #print(produits_par_client_tries)

    # Calculer le nombre de vente total de chaque produit
    ventes_par_produit = ventes.values('produit').annotate(nombre_ventes=Count('id'))
    # Calculer le nombre total de ventes pour tous les produits
    total_ventes = ventes.count()
    # Calculer le chiffre d'affaires total pour tous les produits
    chiffre_affaires_total = ventes.aggregate(total_chiffre_affaires=Sum('prix'))['total_chiffre_affaires']
    # Calculer les statistiques pour chaque produit
    produits_statistiques = []
    for vente_produit in ventes_par_produit:
        produit = vente_produit['produit']
        nombre_ventes = vente_produit['nombre_ventes']
        # Calculer le pourcentage sur le nombre de ventes de tous les produits
        pourcentage_ventes = round((nombre_ventes / total_ventes) * 100,2)
        # Calculer le chiffre d'affaires pour ce produit
        chiffre_affaires_produit = round(ventes.filter(produit=produit).aggregate(total_chiffre_affaires=Sum('prix'))[
            'total_chiffre_affaires'],2)
        # Calculer le pourcentage sur le chiffre d'affaires de tous les produits
        pourcentage_chiffre_affaires = round((chiffre_affaires_produit / chiffre_affaires_total) * 100,2)
        # Ajouter les statistiques du produit à la liste
        produits_statistiques.append({
            'produit': produit,
            'nombre_ventes': nombre_ventes,
            'pourcentage_ventes': float(pourcentage_ventes),
            'chiffre_affaires_produit': float(chiffre_affaires_produit),
            'pourcentage_chiffre_affaires': float(pourcentage_chiffre_affaires),
        })
    #print(produits_statistiques)
    if somme_soldes_negatifs == None:
        somme_soldes_negatifs = 0
    if somme_soldes_positifs==None:
        somme_soldes_positifs=0
    if total_encaissements==None:
        total_encaissements=0
    if chiffre_affaires_total == None:
        chiffre_affaires_total = 0
    data = {
        'total_neg':round(somme_soldes_negatifs,2),
        'total_pos':round(somme_soldes_positifs,2),
        'encaissement':round(total_encaissements,2),
        'nb_vente':total_ventes,
        'chiffrea':round(chiffre_affaires_total,2),
        'cotisants_negatif': cotisants_negatifs,
        'dataDates': DatesStat.objects.all(),
        'dataVentes': ventes,
        'produits_statistiques': produits_statistiques,
        'produits_par_client': produits_par_client_tries,
        'username': request.user.username
    }
    return render(request, 'tresorerie2.html', data)


@login_required
def update_date_debut(request):
    if request.method == "POST":
        selected_date = request.POST.get("selected_date")
        print(selected_date)
        if selected_date:
            if not DatesStat.objects.exists():
                date_debut = datetime.strptime('2023-05-26', '%Y-%m-%d')
                date_fin = datetime.now().date() + timedelta(days=1)
                date_stat = DatesStat(date_debut=date_debut, date_fin=date_fin)
                date_stat.save()
            date_stat = DatesStat.objects.first()  # Récupérer le premier objet DatesStat
            date_stat.date_debut = datetime.strptime(selected_date, '%Y-%m-%d').date()
            date_stat.save()
        return HttpResponseRedirect('/tresorerie')  # Remplacez par l'URL de redirection souhaité
    return redirect('/tresorerie')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

def update_date_fin(request):
    if request.method == "POST":
        selected_date = request.POST.get("selected_date2")
        print(selected_date)
        if selected_date:
            if not DatesStat.objects.exists():
                date_debut = datetime.strptime('2023-05-26', '%Y-%m-%d')
                date_fin = datetime.now().date() + timedelta(days=1)
                date_stat = DatesStat(date_debut=date_debut, date_fin=date_fin)
                date_stat.save()
            date_stat = DatesStat.objects.first()  # Récupérer le premier objet DatesStat
            date_stat.date_fin = datetime.strptime(selected_date, '%Y-%m-%d').date()
            date_stat.date_fin += timedelta(days=1)
            date_stat.save()
        return HttpResponseRedirect('/tresorerie')  # Remplacez par l'URL de redirection souhaité
    return redirect('/tresorerie')  # Rediriger vers la page des stocks si la méthode de requête n'est pas POST

@login_required
def voir_cot(request):
    now = date.today()
    return render(request, 'voircot.html',{'dataCotisants':Cotisants.objects.order_by('nom').all(),'username': request.user.username, 'now':now})
