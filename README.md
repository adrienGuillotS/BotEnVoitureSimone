# BotEnVoitureSimone


Ce dépôt contient un bot développé en **Python 3.12** utilisant **Selenium** pour automatiser des tâches sur la plateforme EVS.

## Structure du projet

- `bot.py` : Le bot. Ce fichier est **à adapter selon vos besoins** pour automatiser les actions spécifiques.
- `passwordcrypt.py` : outil pour **chiffrer vos informations personnelles** (identifiants, mots de passe, etc.). Utile si vous hebergé votre bot sur le cloud.

## Hébergement

J'ai hébergé le bot **sur une machine virtuelle Azure**.

## Prérequis

- Python 3.12
- [Selenium](https://pypi.org/project/selenium/)
- Un navigateur (comme Chrome) avec son **WebDriver** correspondant installé

## 🚀 Installation

```bash
pip install selenium
