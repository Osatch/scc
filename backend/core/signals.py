import unicodedata
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GRDV, ARD2, RelanceJJ

@receiver(post_save, sender=GRDV)
def create_or_update_relancejj_from_grdv(sender, instance, created, **kwargs):
    """
    Lorsqu'un GRDV est créé ou mis à jour, on normalise GRDV.ref_commande
    (les 10 premiers caractères, insensible à la casse) pour chercher un ARD2
    correspondant (ARD2.jeton_commande) et on crée ou met à jour l'instance RelanceJJ.
    """
    if instance.ref_commande:
        ref_norm = unicodedata.normalize("NFKC", instance.ref_commande.strip())[:10]
    else:
        ref_norm = ""
    
    try:
        # Utiliser __iexact pour être insensible à la casse
        ard2_instance = ARD2.objects.get(jeton_commande__iexact=ref_norm)
    except ARD2.DoesNotExist:
        ard2_instance = None

    if ard2_instance:
        relance, created = RelanceJJ.objects.get_or_create(
            grdv=instance,
            jeton=ard2_instance
        )
        relance.save()
    else:
        # Optionnel : loguer ou afficher un message de debug
        print(f"[DEBUG] GRDV id {instance.id} avec ref_norm '{ref_norm}' n'a pas trouvé d'ARD2.")

@receiver(post_save, sender=ARD2)
def create_or_update_relancejj_from_ard2(sender, instance, created, **kwargs):
    """
    Lorsqu'un ARD2 est créé ou mis à jour, on recherche un GRDV dont ref_commande
    correspond (insensible à la casse) à ARD2.jeton_commande et on crée ou met à jour RelanceJJ.
    """
    try:
        grdv_instance = GRDV.objects.get(ref_commande__iexact=instance.jeton_commande)
    except GRDV.DoesNotExist:
        grdv_instance = None

    if grdv_instance:
        relance, created = RelanceJJ.objects.get_or_create(
            grdv=grdv_instance,
            jeton=instance
        )
        relance.save()
    else:
        # Optionnel : log de debug
        print(f"[DEBUG] ARD2 id {instance.id} avec jeton_commande '{instance.jeton_commande}' n'a pas trouvé de GRDV.")
