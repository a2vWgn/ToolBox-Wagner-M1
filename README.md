<h1 align="center">🛡️ ToolBox ScanPy</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
</p>

> ScanPy est une Toolbox pour identifier les failles de sécurité dans les réseaux informatiques. J'ai essayé de faire en sorte d'avoir une ToolBox plutôt complète afin d'avoir une certaine crédibilité professionnel.


## 📟 Fonctionnalité 
<B> - Découverte Réseau :</B> Permet de cartographier le réseau en identifiant les hôtes actifs et les services disponibles sur ces derniers.

<B> - Scan de port :</B> Permet d'analyser les ports ouverts sur une cible spécifique afin de déterminer les points d'accès potentiels.

<B> - Détection de vulnérabilités :</B> Identification des failles de sécurité pour anticiper et corriger les potentielles failles dans le système.

<B> - Tentative de connexion SSH :</B> Utilisation de la liste d’ID/mot de passe rockyou pour effectuer des attaques par force brute sur les connexions SSH.

<B> - Génération de rapport :</B> Création de rapports détaillés sur les vulnérabilités détectées grâce à Nessus, un outil de gestion de la vulnérabilité pour ensuite générer des rapports .PDF.



## 💻 Explication du projet 
<B> - config_parser :</B> Permet de récupérer les paramètres du fichier SCANPI.conf (config du scan nessus et ports)

<B> - nessus_api :</B> Contient toutes les fonctions permettant de lancer un scan, et interagit spécifiquement avec NESSUS web (requête web)

<B> - scan :</B> Toute les fonctions permettant de lancer le scan NESSUS

<B> - github/workflow :</B> Analyse statique et stylistique (avoir un code claire et lisible) des codes

<B> - port_scanner :</B> Script de scan de port

<B> - template :</B> Template du rapport de scan

<B> - .gitignore :</B> Fichier temporaire (on s'en fiche)

<B> - main.py :</B> Premier fichier permettant de tout charger avec les différentes options

<B> - requierement.py :</B> Liste des outils à installer au préalable pour faire marcher la ToolBox

<B> - scanpy.conf :</B> Configuration des différents types de scans réseau et de vulnérabilités
            




## ⚒️ Prérequis d'installation

Certains outils sont nécessaires pour mettre en place la ToolBox. Pour les installer, exécutez les commandes suivantes qui permettent de télécharger tout le nécessaire (requierements.txt) plus simplement  :

```sh
python -m pip install -r requirements.txt
sudo apt install wkhtmltopdf -y
```


## 📋 Utilisation

```sh
Utilisation: main.py [-h] [-v] [-p] [-i IP] [-u USERNAME] [-pw PASSWORD]

Sélectionner nmap ou nessus en fonction de l'option sélectionné.

options:
  -h, --help            Afficher ce message d'aide et quitter
  -v, --vuln_scan       Effectuer une analyse de vulnérabilité à l'aide de Nessus
  -p, --port_scan       Effectuez un balayage des ports à l'aide de nmap.
  -i IP, --ip IP        L'adresse IP à analyser.
  -u USERNAME, --username USERNAME
                        Le nom d'utilisateur à utiliser pour l'analyse de vulnérabilité.
  -pw PASSWORD, --password PASSWORD
                        Le mot de passe à utiliser pour l'analyse de vulnérabilité.
```




