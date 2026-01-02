#!/bin/bash

echo "🔧 Installation de Chrome et des dépendances..."

# Mettre à jour les paquets
apt-get update

# Installer les dépendances nécessaires
apt-get install -y wget unzip curl gnupg

# Ajouter la clé GPG de Google
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Ajouter le repository Chrome
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Mettre à jour et installer Chrome
apt-get update
apt-get install -y google-chrome-stable

# Installer les dépendances Python
pip install -r requirements.txt

echo "✅ Installation terminée"
