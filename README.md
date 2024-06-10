<h1 align="center">ToolBox ScanPy</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
</p>

> ScanPy est une Toolbox pour identifier les failles de sécurité dans les réseaux informatiques. J'ai essayé de faire en sorte d'avoir une ToolBox plutôt complète afin d'avoir une certaine crédibilité professionnel.
## Exigences

Certains outils sont nécessaires pour mettre en place la ToolBox. Pour les installer, exécutez les commandes suivantes qui permettent de télécharger tout le nécessaire plus simplement :

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

