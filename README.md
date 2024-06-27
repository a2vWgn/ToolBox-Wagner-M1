<h1 align="center">🛡️ ToolBox ScanPy</h1>

<br>
<br>

> ScanPy est une Toolbox pour identifier les failles de sécurité dans les réseaux informatiques. J'ai essayé de faire en sorte d'avoir une ToolBox plutôt complète afin d'avoir une certaine crédibilité professionnelle. Possibilité d'installation sur UNIX/Linux et Windows
<br>
<br>

## 📟 Fonctionnalité 
- <B>Découverte Réseau :</B> Permet de cartographier le réseau en identifiant les hôtes actifs et les services disponibles sur ces derniers.

- <B>Scan de port :</B> Permet d'analyser les ports ouverts sur une cible spécifique afin de déterminer les points d'accès potentiels.

- <B>Détection de vulnérabilités :</B> Identification des failles de sécurité pour anticiper et corriger les potentielles failles dans le système.

- <B> Attaque par BruteForce SSH :</B> Utilisation de la liste d’ID/mot de passe rockyou pour effectuer des attaques par force brute sur les connexions SSH.

- <B>Surveillance de commandes sur des machines distantes:</B> Permet d'avoir une visibilité sur toutes les commandes effectuées sur des machines distantes afin de s'assurer qu'aucune activité malveillante est en cours.

- <B>Attaque DDoS :</B> Simule des attaques DDoS pour tester la résistance de votre réseau contre des surcharges massives de trafic. Deux types d'attaques : Flood et No-Flood

- <B>Génération de rapport :</B> Création de rapports détaillés sur les vulnérabilités détectées grâce à Nessus, un outil de gestion des vulnérabilités mais également la création de rapports .PDF pour chaque fonctionnalité (sauf DDoS et BruteForce).

<br>

## 💻 Explication du projet 

- <B>main.py :</B> Point d'entrée qui lit la configuration, définit les arguments et lance les scans de ports, vulnérabilités, attaques SSH, et autres fonctionnalités comme le scan réseau local et l'attaque DDoS.

- <B>app2.py :</B> Point d'entrée pour l'interface graphique. Il utilise la bibliothèque <b>customtkinter</b> pour fournir une interface utilisateur permettant de sélectionner et d'exécuter différentes fonctionnalités comme les scans de ports, les scans de vulnérabilités, les attaques brute force SSH, la surveillance des commandes, les scans de réseau local et les attaques DDoS. Les résultats sont affichés directement dans l'interface graphique et peuvent peuvent être directement affiché et exporté en fichiers PDF 😊

- <b>scanpy.conf :</b> Fichier de configuration contenant les paramètres par défaut pour les scans de ports et de vulnérabilités. Possibilité de modifier les ID/mdp pour accéder à la console Nessus Web.

- <B>scan.py :</B> Gère les interactions avec l'API Nessus pour initialiser, lancer, mettre en pause, reprendre, arrêter les scans et exporter les résultats.

- <B>ports.py :</B> Utilise nmap pour scanner les ports, récupère les informations sur les services et exporte les résultats en PDF.

- <B>nessus_api.py :</B>  Gère l'authentification et les interactions avec l'API Nessus, y compris la création, le lancement et l'exportation des résultats des scans via des requêtes web.

- <B>parser.py :</B> Interface simplifiée autour de configparser pour lire les valeurs des paramètres du fichier de configuration. Il permet de gérer facilement les paramètres de configuration utilisés dans les autres scripts.

- <B>ssh.py :</B> Effectue des attaques par force brute SSH en utilisant paramiko et la liste de mots de passe rockyou.txt.

- <B>command_monitor.py :</B> Permet la surveillance des commandes exécutées sur une machine distante via SSH. Les commandes sont enregistrées dans un fichier local pour analyse ultérieure.

- <B>ddos_attack.py :</B> Simule des attaques DDoS pour tester la résistance d'un réseau contre des surcharges massives de trafic. Permet de choisir entre le mode flood et non-flood

- <B>network_scan.py :</B> Permet de cartographier le réseau localement en identifiant les hôtes actifs (Adresses IP et MAC) et les services disponibles sur ces derniers. Les résultats sont exportés en fichiers PDF

- <B>requirement.txt :</B> Liste des outils à installer au préalable pour faire marcher la ToolBox.

- <B>template :</B> Contient les templates HTML utilisés pour générer les rapports PDF pour les différentes fonctionnalités de scan et de surveillance.

- <B>.gitignore :</B> Fichier temporaire (on s'en fiche).

- <B>github/workflow :</B> Contient les configurations pour les analyses statiques et stylistiques (pylint, flake8, black, isort, mypy) pour s'assurer que le code est clair et lisible.

<br>
<br>
<br>

<B>1. Initialisation et arguments :</B> Le fichier main.py initialise le processus en fonction des arguments fournis et permet l'exécution des différentes fonctionnalités via une interface en ligne de commande. Le fichier app2.py, quant à lui, offre une interface graphique intuitive pour accéder aux mêmes fonctionnalités de manière plus conviviale.

<B>2. Configuration :</B> main.py lit les paramètres de scanpy.conf en utilisant parser.py.

<B>3. Scan de ports :</B> main.py utilise ports.py pour effectuer le scan et exporter les résultats.

<B>4. Scan de vulnérabilités :</B> main.py utilise scan.py pour interagir avec l'API Nessus via nessus_api.py.

<B>5. Bruteforce SSH :</B> main.py utilise ssh.py pour tenter les connexions avec paramiko.

<B>6. Scan réseau local :</B> main.py utilise network_scan.py pour identifier les hôtes actifs et les services disponibles et exporter les résultats en PDF.

<B>7. Attaque DDoS :</B> main.py utilise ddos_attack.py pour simuler des attaques DDoS.

<B>8. Surveillance des commandes :</B> main.py utilise command_monitor.py pour surveiller et enregistrer les commandes exécutées sur une machine cible via SSH.

<B>9. Gestion des résultats :</B> Les résultats sont sauvegardés et exportés en PDF dans le dossier <B>results</B>, avec le chemin indiqué pour chaque fonctionnalité.

<br>

## ⚒️ Prérequis d'installation

Certains outils sont nécessaires pour mettre en place la ToolBox. Pour les installer, exécutez les commandes suivantes qui permettent de télécharger tout le nécessaire (requirements.txt) plus simplement :

<B>Sur Linux :</B>
```sh
python -m pip install -r requirements.txt
sudo apt install wkhtmltopdf -y
```
<br>
 <B>Sur Windows :</B><br>
 Installer Python 3 : https://www.python.org/downloads/ puis l'ajouter à votre variable d'environnement PATH<br>
 Installer wkhtmltoppdf : https://wkhtmltopdf.org/ puis l'ajouter à votre variable d'environnement PATH<br>
 <br>
 Maintenant en PowerShell, installer le fichier requierement.txt :
 <br>
 
```sh
python -m pip install -r requirements.txt
```
 
## 📋 Comment ça marche ?

Une fois l'entité du projet installée, il faudra se rendre dans le répertoire en question. Une fois dedans :

- Nous pouvons utiliser l'interface en ligne de commande :
```sh
python main.py
```
<br>
<p align="center">
<img src="https://github.com/a2vWgn/ToolBox-Wagner-M1/blob/master/template/interface.png?raw=true" alt="Interface" />
</p>
<br>
<br>

- Nous pouvons utiliser l'interface graphique :
```sh
python app2.py
```
<p align="center">
<img src="https://github.com/a2vWgn/ToolBox-Wagner-M1/blob/master/template/app.png?raw=true" alt="App" />
  </p>
  
<br>
<p align="center">
Maintenant, nous n'avons plus qu'à sélectionner la fonctionnalité que nous souhaitons exécuter !
</p>

