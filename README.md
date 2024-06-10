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

<br>


## 💻 Explication du projet 

<B> - main.py :</B> Point d'entrée qui lit la configuration, définit les arguments et lance les scans de ports, vulnérabilités ou attaques SSH.

<b> - scanpy.conf :</b>Fichier de configuration contenant les paramètres par défaut pour les scans de ports et de vulnérabilités. <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ici les ID/MDP pour accèder à la console Nessus Web sont vierges. On peut donc choisir les identifiants à notre convenance 😊

<B> - scan.py :</B> Gère les interactions avec l'API Nessus pour initialiser, lancer, mettre en pause, reprendre, arrêter les scans et exporter les résultats.

<B> - ports.py :</B> scan.py : Utilise nmap pour scanner les ports, récupère les informations sur les services et exporte les résultats en PDF.

<B> - nessus_api.py :</B>  Gère l'authentification et les interactions avec l'API Nessus, y compris la création, le lancement et l'exportation des résultats des scans via des requêtes web

<B> - parser.py :</B> Wrapper autour de configparser pour lire les valeurs des paramètres du fichier de configuration.

<B> - ssh.py :</B> Effectue des attaques par force brute SSH en utilisant paramiko et la liste de mots de passe rockyou.txt.

<B> - requierement.py :</B> Liste des outils à installer au préalable pour faire marcher la ToolBox

<B> - template :</B> Template du rapport de scan pdf

<B> - .gitignore :</B> Fichier temporaire (on s'en fiche)

<B> - github/workflow :</B> Analyse statique et stylistique (avoir un code claire et lisible) des codes avec pylint, flake8, black, isort, et mypy.

<br>
<br>
<br>

<B>1. Initialisation et arguments :</B> main.py initialise le processus en fonction des arguments fournis.

<B>2. Configuration :</B> main.py lit les paramètres de scanpy.conf en utilisant parser.py.

<B>3. Scan de ports :</B> main.py utilise ports.py pour effectuer le scan et exporter les résultats.

<B>4. Scan de vulnérabilités :</B> main.py utilise scan.py pour interagir avec l'API Nessus via nessus_api.py.

<B>5. Bruteforce SSH :</B> main.py utilise ssh.py pour tenter les connexions avec paramiko.

<B>6. Gestion des résultats :</B> Les résultats sont sauvegardés et exportés en PDF ou autres formats.

<br>




## ⚒️ Prérequis d'installation

Certains outils sont nécessaires pour mettre en place la ToolBox. Pour les installer, exécutez les commandes suivantes qui permettent de télécharger tout le nécessaire (requierements.txt) plus simplement  :

```sh
python -m pip install -r requirements.txt
sudo apt install wkhtmltopdf -y
```
<br>
<br>

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
<br>


## 👨‍💻 Exemples de commandes 

<B>Afficher le message d'aide:</B>
```sh
python main.py -h
```

<B>Scan de Ports avec NMAP sur adresse IP unique: </B>
```sh
python main.py -p -i 192.168.1.1
```

<B>Scan de Ports avec NMAP sur plage d'adresses IP: </B>
```sh
python main.py -p -i 192.168.1.1-192.168.1.254
```

<B>Scan de Vulnérabilité avec Nessus sur adresse IP unique en connaissance de ID/MDP: </B>
```sh
python main.py -v -i 192.168.1.1 -u admin -pw password123
```

<B>Scan de Vulnérabilité avec Nessus sur plage d'adresses IP en connaissance de ID/MDP: </B>
```sh
python main.py -v -i 192.168.1.1-192.168.1.254 -u admin -pw password123
```

<B>Scan de Vulnérabilité sur plusieurs plage d'adresses IPs en connaissance de ID/MDP: </B>
```sh
python main.py -v -i 192.168.1.1-192.168.1.50 -u admin -pw password123
python main.py -v -i 192.168.2.1-192.168.2.50 -u admin -pw password123
```

<B>Scan de ports sur plusieurs plages d'IPs: </B>
```sh
python main.py -p -i 192.168.1.1-192.168.1.50
python main.py -p -i 192.168.2.1-192.168.2.50
```
