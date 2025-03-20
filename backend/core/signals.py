from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GRDV, ARD2, RelanceJJ

@receiver(post_save, sender=GRDV)
def create_or_update_relancejj_from_grdv(sender, instance, created, **kwargs):
    """
    Lorsqu'un GRDV est créé ou mis à jour, on vérifie s'il existe un ARD2 correspondant 
    (en comparant par exemple GRDV.ref_commande et ARD2.jeton_commande) et on crée ou met à jour RelanceJJ.
    """
    # On essaie de récupérer l'instance ARD2 associée
    try:
        ard2_instance = ARD2.objects.get(jeton_commande=instance.ref_commande)
    except ARD2.DoesNotExist:
        ard2_instance = None

    # On crée ou met à jour RelanceJJ en utilisant le GRDV et l'ARD2 récupéré
    relance, created = RelanceJJ.objects.get_or_create(
        grdv=instance,
        jeton=ard2_instance
    )
    # Appel de save() qui synchronise les données depuis GRDV et ARD2
    relance.save()

@receiver(post_save, sender=ARD2)
def create_or_update_relancejj_from_ard2(sender, instance, created, **kwargs):
    """
    Lorsqu'un ARD2 est créé ou mis à jour, on recherche un GRDV correspondant 
    et on crée ou met à jour RelanceJJ.
    """
    try:
        grdv_instance = GRDV.objects.get(ref_commande=instance.jeton_commande)
    except GRDV.DoesNotExist:
        grdv_instance = None

    if grdv_instance:
        relance, created = RelanceJJ.objects.get_or_create(
            grdv=grdv_instance,
            jeton=instance
        )
        relance.save()
