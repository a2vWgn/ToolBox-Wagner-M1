<h1 align="center">ToolBox ScanPy</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
</p>

> ScanPy est une Toolbox pour identifier les failles de sécurité dans les réseaux informatiques. J'ai essayé de faire en sorte d'avoir une ToolBox plutôt complète afin d'avoir une certaine crédibilité professionnel.


## Fonctionnalité 
 - Découverte Réseau : Permet de cartographier le réseau en identifiant les hôtes actifs et les services disponibles sur ces derniers.
 - Scan de port : Permet d'analyser les ports ouverts sur une cible spécifique afin de déterminer les points d'accès potentiels.
 - Détection de vulnérabilités : Identification des failles de sécurité pour anticiper et corriger les potentielles failles dans le système.
 - Tentative de connexion SSH : Utilisation de la liste d’ID/mot de passe rockyou pour effectuer des attaques par force brute sur les connexions SSH.
 - Génération de rapport : Création de rapports détaillés sur les vulnérabilités détectées grâce à Nessus, un outil de gestion de la vulnérabilité pour ensuite générer des rapports .PDF.



## Exigences d'installation

Certains outils sont nécessaires pour mettre en place la ToolBox. Pour les installer, exécutez les commandes suivantes qui permettent de télécharger tout le nécessaire (requierements.txt) plus simplement  :

```sh
python -m pip install -r requirements.txt
sudo apt install wkhtmltopdf -y
```

## Utilisation

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




