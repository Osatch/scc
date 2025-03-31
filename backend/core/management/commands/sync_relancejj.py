import unicodedata
from django.core.management.base import BaseCommand
from core.models import GRDV, ARD2, RelanceJJ, Parametres  # Assurez-vous que les modèles sont correctement importés

class Command(BaseCommand):
    help = ("Synchronise les données de GRDV et ARD2 dans RelanceJJ en mettant à jour si le jeton_commande et la date_rdv "
            "correspondent à une entrée existante, sinon crée une nouvelle ligne. "
            "Ensuite, met à jour le numéro technicien et la société à partir de Parametres.")

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

            # Détermination de la date du RDV à partir de GRDV (si elle existe)
            date_rdv = grdv.date_rdv.date() if grdv.date_rdv else None

            # Préparation des valeurs à mettre à jour/créer dans RelanceJJ
            defaults = {
                "grdv": grdv,  # Association à GRDV
                "heure_debut": ard2_instance.debut_intervention.time() if ard2_instance.debut_intervention else None,
                "heure_fin": ard2_instance.fin_intervention.time() if ard2_instance.fin_intervention else None,
                "departement": ard2_instance.departement if ard2_instance.departement else None,
                "techniciens": ard2_instance.technicien  # Affecte techniciens de RelanceJJ avec technicien de ARD2
            }

            # Recherche dans RelanceJJ avec jeton_commande ET date_rdv
            relance_qs = RelanceJJ.objects.filter(
                jeton_commande=ard2_instance.jeton_commande,
                date_rdv=date_rdv
            )

            if relance_qs.exists():
                # Si une entrée correspondante existe, on la met à jour
                relance = relance_qs.first()
                for key, value in defaults.items():
                    setattr(relance, key, value)
                relance.save()
                action = "Mis à jour"
            else:
                # Sinon, on crée une nouvelle entrée
                defaults.update({
                    "jeton_commande": ard2_instance.jeton_commande
                })
                relance = RelanceJJ.objects.create(**defaults)
                action = "Créé"

            self.stdout.write(self.style.SUCCESS(f"{action} RelanceJJ pour GRDV {grdv.id} (date_rdv: {date_rdv})"))

            # Synchronisation du numéro technicien et de la société à partir de la table Parametres.
            param = Parametres.objects.filter(
                nom_tech__iexact=relance.techniciens,
                departement__iexact=relance.departement
            ).first()

            if param:
                if param.numero_technicien:
                    relance.numero = param.numero_technicien
                if param.societe:
                    relance.societe = param.societe
                relance.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Mis à jour le numéro technicien et la société pour RelanceJJ de GRDV {grdv.id} (numéro: {param.numero_technicien}, société: {param.societe})"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Aucun paramètre trouvé pour technicien '{relance.techniciens}' et département '{relance.departement}' pour GRDV {grdv.id}"
                ))
