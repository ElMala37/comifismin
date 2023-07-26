from django.contrib import admin
from django.urls import path

from AppCotisants.views import CustomLoginView
from accueil import views
from AppCotisants import views as views2
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout',
         kwargs={'next_page': '/'}),
    path('admin/', admin.site.urls),
    path('welcome/', views2.welcome),
    path('', views.accueil),
    path('ajtcotisants/', views2.index),
    path('gstsoldes/', views2.index2),
    path('gstfavoris/', views2.gstfavoris),
    path('gstcotisants/', views2.mod_cst),
    path('update_solde/', views2.update_solde, name='update_solde'),
    path('update_duree/', views2.update_duree, name='update_duree'),
    path('supcotisants/', views2.index3),
    path('delete_cotisant/', views2.delete_cotisant, name='delete_cotisant'),
    path('voirsupcot/', views2.voirsupcot),
    path('ajtproduits/', views2.ajtproduits),
    path('gstproduits/', views2.index4),
    path('update_stock/', views2.update_stock, name='update_stock'),
    path('ajt_favoris_tb/', views2.ajt_favoris_tb, name='ajt_favoris_tb'),
    path('del_favoris_tb/', views2.del_favoris_tb, name='del_favoris_tb'),
    path('ajt_favoris_tp/', views2.ajt_favoris_tp, name='ajt_favoris_tp'),
    path('del_favoris_tp/', views2.del_favoris_tp, name='del_favoris_tp'),
    path('supproduits/', views2.index5),
    path('delete_produit/', views2.delete_produit, name='delete_produit'),
    path('type_produits/', views2.type_produits),
    path('ajt_type/', views2.ajt_type, name='ajt_type'),
    path('del_type/', views2.del_type, name='del_type'),
    path('type_paiements/', views2.type_paiements),
    path('ajt_modep/', views2.ajt_modep, name='ajt_modep'),
    path('del_modep/', views2.del_modep, name='del_modep'),
    path('promo/', views2.promo),
    path('ajt_promo/', views2.ajt_promo, name='ajt_promo'),
    path('del_promo/', views2.del_promo, name='del_promo'),
    path('ajtvente/', views2.ajouter_vente),
    path('final_vente/', views2.final_vente, name='final_vente'),
    path('voirventes/', views2.voir_ventes),
    path('delete_vente/', views2.delete_vente, name='delete_vente'),
    path('voirencaissements/', views2.voir_encaissement),
    path('voirajtproduits/', views2.voir_ajoutstock),
    path('voirconnexions/', views2.voir_cnx),
    path('voirsupvente/', views2.voir_supvente),
    path('tresorerie/', views2.tresorerie),
    path('voircot/', views2.voir_cot),
    path('update_date_debut/', views2.update_date_debut, name='update_date_debut'),
    path('update_date_fin/', views2.update_date_fin, name='update_date_fin'),
]
