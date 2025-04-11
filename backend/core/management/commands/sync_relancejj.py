import unicodedata
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import GRDV, ARD2, RelanceJJ, Parametres


class Command(BaseCommand):
    help = (
        "Synchronise les données GRDV + ARD2 dans RelanceJJ pour la journée actuelle.\n"
        "- Si une ligne existe avec même jeton_commande + date_rdv => mise à jour.\n"
        "- Sinon => création.\n"
        "- Met ensuite à jour le numéro technicien + société à partir de Parametres."
    )

    def handle(self, *args, **kwargs):
        today = timezone.localdate()

        ard2_values = list(ARD2.objects.values_list('jeton_commande', flat=True))
        self.stdout.write(self.style.NOTICE(f"🔍 ARD2 présents : {len(ard2_values)}"))
        self.stdout.write(self.style.NOTICE(f"Exemples : {ard2_values[:5]}"))

        count_created = 0
        count_updated = 0

        # 🔄 On ne traite que les GRDV dont la date_rdv est aujourd'hui
        grdv_qs = GRDV.objects.filter(date_rdv__date=today)

        self.stdout.write(self.style.NOTICE(f"🗓️ Nombre de GRDV à la date {today} : {grdv_qs.count()}"))

        for grdv in grdv_qs:
            if not grdv.ref_commande:
                self.stdout.write(self.style.WARNING(f"⚠️ GRDV {grdv.id} sans ref_commande. Ignoré."))
                continue

            # Normalisation du jeton
            ref_norm = unicodedata.normalize("NFKC", grdv.ref_commande.strip())[:10]
            self.stdout.write(f"\n🔗 GRDV {grdv.id} → ref_commande normalisé : {ref_norm}")

            ard2 = ARD2.objects.filter(jeton_commande__iexact=ref_norm).first()
            if not ard2:
                self.stdout.write(self.style.WARNING(f"❌ Aucun ARD2 trouvé pour ref '{ref_norm}'"))
                continue

            date_rdv = grdv.date_rdv.date() if grdv.date_rdv else None

            # Synchronisation logique : on ne prend "NOK" comme réel que si début ET fin sont présents
            etat_intervention = ard2.etat_intervention or ''
            if etat_intervention.upper() == "NOK":
                if not (ard2.debut_intervention and ard2.fin_intervention):
                    etat_intervention = ""  # On ignore les NOK fantômes

            relance_data = {
                "grdv": grdv,
                "heure_debut": ard2.debut_intervention.time() if ard2.debut_intervention else None,
                "heure_fin": ard2.fin_intervention.time() if ard2.fin_intervention else None,
                "departement": ard2.departement or '',
                "techniciens": ard2.technicien or '',
                "synchro": etat_intervention,  # ⬅️ état nettoyé selon ta logique
            }

            relance_qs = RelanceJJ.objects.filter(
                jeton_commande=ard2.jeton_commande,
                date_rdv=date_rdv
            )

            if relance_qs.exists():
                relance = relance_qs.first()
                for key, val in relance_data.items():
                    setattr(relance, key, val)
                relance.save()
                count_updated += 1
                action = "📝 Mis à jour"
            else:
                relance = RelanceJJ.objects.create(
                    jeton_commande=ard2.jeton_commande,
                    date_rdv=date_rdv,
                    **relance_data
                )
                count_created += 1
                action = "🆕 Créé"

            self.stdout.write(self.style.SUCCESS(f"{action} RelanceJJ pour GRDV {grdv.id}"))

            # Mise à jour via Parametres
            param = Parametres.objects.filter(
                nom_tech__iexact=relance.techniciens,
                departement__iexact=relance.departement
            ).first()

            if param:
                changed = False
                if param.numero_technicien and relance.numero != param.numero_technicien:
                    relance.numero = param.numero_technicien
                    changed = True
                if param.societe and relance.societe != param.societe:
                    relance.societe = param.societe
                    changed = True

                if changed:
                    relance.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"🔄 Numéro/Société mis à jour : {param.numero_technicien} / {param.societe}"
                    ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"⚠️ Aucun Parametres pour '{relance.techniciens}' - {relance.departement}"
                ))

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Synchronisation terminée : {count_created} créés, {count_updated} mis à jour."
        ))
