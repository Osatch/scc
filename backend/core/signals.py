import unicodedata
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GRDV, ARD2, RelanceJJ, Parametres,ImportARDLog 


@receiver(post_save, sender=GRDV)
def create_or_update_relancejj_from_grdv(sender, instance, created, **kwargs):
    if not instance.ref_commande:
        return

    ref_norm = unicodedata.normalize("NFKC", instance.ref_commande.strip())[:10]
    ard2_instance = ARD2.objects.filter(jeton_commande__iexact=ref_norm).first()
    if not ard2_instance:
        return

    date_rdv = instance.date_rdv.date() if instance.date_rdv else None
    if not date_rdv:
        return

    relance, _ = RelanceJJ.objects.update_or_create(
        jeton_commande=ard2_instance.jeton_commande,
        date_rdv=date_rdv,
        defaults={
            "grdv": instance,
            "heure_debut": ard2_instance.debut_intervention.time() if ard2_instance.debut_intervention else None,
            "heure_fin": ard2_instance.fin_intervention.time() if ard2_instance.fin_intervention else None,
            "departement": ard2_instance.departement,
            "techniciens": ard2_instance.technicien,
        }
    )

    # Enrichir depuis Parametres
    param = Parametres.objects.filter(
        nom_tech__iexact=relance.techniciens,
        departement__iexact=relance.departement
    ).first()
    if param:
        relance.numero = param.numero_technicien
        relance.societe = param.societe
        relance.save()


@receiver(post_save, sender=ARD2)
def create_or_update_relancejj_from_ard2(sender, instance, created, **kwargs):
    grdv_instance = GRDV.objects.filter(ref_commande__iexact=instance.jeton_commande).first()
    if not grdv_instance:
        return

    date_rdv = grdv_instance.date_rdv.date() if grdv_instance.date_rdv else None
    if not date_rdv:
        return

    relance, _ = RelanceJJ.objects.update_or_create(
        jeton_commande=instance.jeton_commande,
        date_rdv=date_rdv,
        defaults={
            "grdv": grdv_instance,
            "heure_debut": instance.debut_intervention.time() if instance.debut_intervention else None,
            "heure_fin": instance.fin_intervention.time() if instance.fin_intervention else None,
            "departement": instance.departement,
            "techniciens": instance.technicien,
        }
    )

    param = Parametres.objects.filter(
        nom_tech__iexact=relance.techniciens,
        departement__iexact=relance.departement
    ).first()
    if param:
        relance.numero = param.numero_technicien
        relance.societe = param.societe
        relance.save()
