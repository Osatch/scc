from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import GRDV, ARD2, RelanceJJ

@receiver(post_save, sender=GRDV)
def create_or_update_relancejj_from_grdv(sender, instance, created, **kwargs):
    """
    À chaque sauvegarde d'une instance GRDV, on cherche l'ARD2 correspondant
    (en comparant GRDV.ref_commande et ARD2.jeton_commande) pour mettre à jour ou créer RelanceJJ.
    """
    try:
        ard2 = ARD2.objects.get(jeton_commande=instance.ref_commande)
    except ARD2.DoesNotExist:
        ard2 = None

    # On ne crée RelanceJJ que si un ARD2 correspondant est trouvé
    if ard2:
        relance, created = RelanceJJ.objects.update_or_create(
            grdv=instance,
            jeton=ard2,
            defaults={}
        )
        # Appeler save() permet à RelanceJJ de synchroniser ses champs via son propre .save()
        relance.save()

@receiver(post_save, sender=ARD2)
def create_or_update_relancejj_from_ard2(sender, instance, created, **kwargs):
    """
    À chaque sauvegarde d'une instance ARD2, on cherche l'instance GRDV associée
    (en comparant ARD2.jeton_commande et GRDV.ref_commande) pour créer ou mettre à jour RelanceJJ.
    """
    try:
        grdv = GRDV.objects.get(ref_commande=instance.jeton_commande)
    except GRDV.DoesNotExist:
        grdv = None

    if grdv:
        relance, created = RelanceJJ.objects.update_or_create(
            grdv=grdv,
            jeton=instance,
            defaults={}
        )
        relance.save()
