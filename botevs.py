
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback


load_dotenv()

MOIS = {
    "janvier": 1,
    "février": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "août": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "décembre": 12,
}

# Configuration pour l'envoi d'emails
smtp_address = "smtp.gmail.com"
smtp_port = 465
email_address = os.getenv("email_address")
email_password = os.getenv("email_password")
email_receiver = os.getenv("email_receiver")
email_evs = os.getenv("email_evs")
mdp_evs = os.getenv("mdp_evs")

# Variable globale pour stocker la dernière date envoyée
last_sent_date = None


def send_email_ssl(date_cours, error=None):
    """Envoyer un email via Gmail avec SSL"""
    global last_sent_date

    # Si c'est la même date que la dernière fois, ne pas envoyer d'email
    if not error and date_cours == last_sent_date:
        print(f"ℹ️ Un email a déjà été envoyé pour la date {date_cours}")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = email_address
        msg["To"] = email_receiver

        if error:
            msg["Subject"] = "⚠️ Erreur - Bot En Voiture Simone"
            body = f"""
Le bot a rencontré une erreur:

{error}

Le bot continue de fonctionner et réessaiera dans 5 minutes.
            """
        else:
            msg["Subject"] = "Disponibilité détectée - En Voiture Simone"
            body = f"""
Une disponibilité a été détectée pour un cours de conduite!

📅 Date disponible: {date_cours}

Cette date est avant le 9 janvier 2026.
Connectez-vous rapidement pour réserver ce créneau!

Lien: https://app.envoituresimone.com/

Cordialement,
Votre assistant de réservation
            """

        msg.attach(MIMEText(body, "plain"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
            server.login(email_address, email_password)
            server.send_message(msg)

        print("Email envoyé avec succès!")

        # Mémoriser la date pour laquelle on vient d'envoyer un email
        if not error:
            last_sent_date = date_cours

    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")


def parse_date(date_text):
    """Parse une date en français"""
    try:
        # Format attendu: "Lundi 3 mars"
        jour, numero, mois = date_text.lower().split()

        # Convertir le mois en numéro
        mois_num = MOIS.get(mois)
        if not mois_num:
            raise ValueError(f"Mois non reconnu: {mois}")

        # Créer la date
        return datetime(2025, mois_num, int(numero))
    except Exception as e:
        print(f"❌ Erreur lors du parsing de la date: {e}")
        return None


def check_disponibilites():
    """Fonction principale qui vérifie les disponibilités"""
    try:
        # Configuration du navigateur pour Replit
        chrome_options = Options()
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        chrome_options.add_argument("--headless")  # Mode sans interface graphique
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Lancer le navigateur
        browser = webdriver.Chrome(options=chrome_options)

        browser.set_page_load_timeout(60)

        try:
            # Définir un timeout plus long pour les requêtes
            browser.set_page_load_timeout(60)  # Augmenter le timeout à 60 secondes

            # Ouvrir la page de connexion
            browser.get("https://app.envoituresimone.com/login/signIn")
            time.sleep(5)

            # Remplir l'email
            try:
                email_input = browser.find_element(By.ID, "siginInEmail")
                email_input.click()
                email_input.send_keys(email_evs)
                print("✅ Email rempli")
            except Exception as e:
                print(f"❌ Erreur champ email : {e}")
                raise e

            # Remplir le mot de passe
            try:
                password_input = browser.find_element(By.ID, "signinPassword")
                password_input.click()
                time.sleep(1)
                password_input.send_keys(mdp_evs)
                print("✅ Mot de passe rempli")
            except Exception as e:
                print(f"❌ Erreur champ mot de passe : {e}")
                raise e

            # Cliquer sur "Me connecter"
            try:
                submit_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "btn"))
                )
                submit_button.click()
                print("✅ Connexion envoyée")
            except Exception as e:
                print(f"❌ Erreur bouton connexion : {e}")
                raise e

            # Attendre le chargement après connexion
            time.sleep(5)

            # Cliquer sur "Plus tard" si visible
            try:
                plus_tard_button = WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable(
                        (By.CLASS_NAME, "btn.full-width.light.margin-top-10")
                    )
                )
                plus_tard_button.click()
                print("✅ 'Plus tard' cliqué")
            except Exception:
                print("⚠️ 'Plus tard' non trouvé ou ignoré")

            # Fermer la pop-up - Méthode améliorée
            try:
                # Attendre plus longtemps pour le pop-up
                time.sleep(3)

                # Première tentative - par classe
                try:
                    close_button = WebDriverWait(browser, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "close-modal"))
                    )
                    close_button.click()
                    print("✅ Pop-up fermée (méthode 1)")
                except:
                    # Deuxième tentative - par XPath
                    try:
                        close_button = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//*[contains(@class, 'close-modal')]")
                            )
                        )
                        browser.execute_script("arguments[0].click();", close_button)
                        print("✅ Pop-up fermée (méthode 2)")
                    except:
                        # Troisième tentative - chercher un bouton avec JavaScript
                        try:
                            browser.execute_script(
                                """
                                var elements = document.getElementsByClassName('close-modal');
                                if(elements.length > 0) elements[0].click();
                            """
                            )
                            print("✅ Pop-up fermée (méthode 3)")
                        except:
                            print("⚠️ Aucune méthode n'a réussi à fermer le pop-up")

            except Exception as e:
                print(f"⚠️ Erreur lors de la tentative de fermeture du pop-up : {e}")

            # Petite pause après la tentative de fermeture
            time.sleep(2)

            # Cliquer sur "Conduite"
            try:
                conduite_button = WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//li[span[contains(text(),'Conduite')]]")
                    )
                )
                conduite_button.click()
                print("✅ 'Conduite' cliqué")
            except Exception:
                print("⚠️ 'Conduite' non trouvé")

            # Cliquer sur "Christophe"
            time.sleep(2)
            try:
                christophe_button = WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//div[contains(@class, 'favTeacherText')]//div[contains(@class, 'favTeacherName') and contains(text(),'Christophe')]",
                        )
                    )
                )
                christophe_button.click()
                print("✅ 'Christophe' cliqué")
            except Exception as e:
                print(f"⚠️ 'Christophe' non trouvé: {e}")
                try:
                    christophe_parent = WebDriverWait(browser, 3).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//div[contains(@class, 'favTeacherText')]")
                        )
                    )
                    christophe_parent.click()
                    print("✅ 'Christophe' cliqué (via parent)")
                except Exception as e2:
                    print(f"⚠️ Échec du clic sur Christophe: {e2}")

            # Attendre avant de continuer
            time.sleep(5)

            # Trouver et cliquer sur "Réserver une leçon"
            print("🔄 Tentative de clic sur 'Réserver une leçon'...")
            try:
                reserver_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//div[contains(@class, 'containerDiv')]//span[contains(text(),'Réserver une leçon')]",
                        )
                    )
                )
                browser.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    reserver_button,
                )
                time.sleep(3)
                browser.execute_script("arguments[0].click();", reserver_button)
                print("✅ 'Réserver une leçon' cliqué avec succès")
            except Exception as e:
                print(f"⚠️ Première tentative échouée: {e}")
                try:
                    reserver_container = WebDriverWait(browser, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//div[contains(@class, 'containerDiv')]")
                        )
                    )
                    browser.execute_script("arguments[0].click();", reserver_container)
                    print("✅ 'Réserver une leçon' cliqué (via container)")
                except Exception as e2:
                    print(f"❌ Erreur lors du clic sur 'Réserver une leçon': {e2}")
                    raise e2

            # Attendre le chargement de la page de réservation
            time.sleep(5)

            # Cliquer sur "1h"
            print("🔄 Tentative de clic sur '1h'...")
            try:
                une_heure_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//span[contains(text(),'1h')]")
                    )
                )
                browser.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    une_heure_button,
                )
                time.sleep(1)
                browser.execute_script("arguments[0].click();", une_heure_button)
                print("✅ '1h' cliqué avec succès")
            except Exception as e:
                print(f"⚠️ Erreur lors du clic sur '1h': {e}")

            # Attendre après le clic sur 1h
            time.sleep(5)

            # Trouver la première date disponible
            premiere_date = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class, 'collapsible-header')]//span[contains(@class, 'collapsible-title')]//span",
                    )
                )
            )
            date_text = premiere_date.text
            print(f"📅 Première date disponible : {date_text}")

            # Parser la date et vérifier
            date_obj = parse_date(date_text)
            if date_obj:
                date_limite = datetime(2026, 1, 21)
                date_initiale = datetime(2026, 1, 7)
                if date_obj < date_limite and date_obj >= date_initiale:
                    print(
                        f"📧 La date {date_text} est avant le 9 janvier, envoi d'un email..."
                    )
                    send_email_ssl(date_text)
                else:
                    print(
                        f"ℹ️ La date {date_text} est après le 9 janvier, pas d'email"
                    )

        except Exception as e:
            error_msg = f"Erreur pendant l'exécution: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            print(error_msg)
            send_email_ssl(None, error=error_msg)
            raise e

        finally:
            # Fermer le navigateur dans tous les cas
            browser.quit()

    except Exception as e:
        print(f"Erreur critique: {e}")


def main():
    print("🤖 Démarrage du bot de surveillance En Voiture Simone")
    print("⏰ Vérification toutes les 5 minutes")

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\n🔄 Nouvelle vérification à {current_time}")

        try:
            check_disponibilites()
        except Exception as e:
            print(f"❌ Erreur lors de la vérification: {e}")

        print("😴 Attente de 5 minutes avant la prochaine vérification...")
        time.sleep(600)  # 5 minutes


if __name__ == "__main__":
    main()