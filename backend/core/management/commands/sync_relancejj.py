import unicodedata
from django.core.management.base import BaseCommand
from core.models import GRDV, ARD2, RelanceJJ

class Command(BaseCommand):
    help = "Synchronise les données de GRDV et ARD2 dans RelanceJJ en mettant à jour si le jeton existe déjà"

    def handle(self, *args, **kwargs):
        # Affichage des valeurs de jeton_commande présentes dans ARD2 pour débogage
        ard2_values = list(ARD2.objects.values_list('jeton_commande', flat=True))
        self.stdout.write(self.style.NOTICE(f"Nombre total d'ARD2 : {len(ard2_values)}"))
        self.stdout.write(self.style.NOTICE(f"Exemple de valeurs ARD2 : {ard2_values[:10]}"))

        for grdv in GRDV.objects.all():
            if not grdv.ref_commande:
                self.stdout.write(self.style.WARNING(
                    f"GRDV {grdv.id} n'a pas de ref_commande définie, passage au suivant."
                ))
                continue

            # Affichage de la valeur brute pour débogage
            self.stdout.write(self.style.NOTICE(
                f"Valeur brute ref_commande pour GRDV {grdv.id} : {repr(grdv.ref_commande)}"
            ))
            
            # Normalisation de ref_commande : suppression des espaces et normalisation Unicode,
            # puis troncature à 10 caractères pour correspondre à ARD2.jeton_commande (varchar(10))
            ref_norm = unicodedata.normalize("NFKC", grdv.ref_commande.strip())[:10]
            self.stdout.write(f"Recherche pour GRDV {grdv.id} avec ref_commande normalisé = '{ref_norm}'")

            # Recherche de l'instance ARD2 correspondante (insensible à la casse)
            ard2_instance = ARD2.objects.filter(jeton_commande__iexact=ref_norm).first()
            if not ard2_instance:
                self.stdout.write(self.style.WARNING(
                    f"GRDV {grdv.id} n'a pas d'ARD2 associé (ref_commande: {ref_norm}), passage au suivant."
                ))
                continue

            # Préparation des valeurs à mettre à jour/créer
            defaults = {
                "heure_debut": ard2_instance.debut_intervention.time() if ard2_instance.debut_intervention else None,
                "heure_fin": ard2_instance.fin_intervention.time() if ard2_instance.fin_intervention else None,
                "departement": ard2_instance.departement if ard2_instance.departement else None,
            }

            # Mise à jour ou création de l'instance RelanceJJ
            relance, created = RelanceJJ.objects.update_or_create(
                grdv=grdv,
                jeton_commande=ard2_instance.jeton_commande,
                defaults=defaults
            )

            action = "Créé" if created else "Mis à jour"
            self.stdout.write(self.style.SUCCESS(f"{action} RelanceJJ pour GRDV {grdv.id}"))
