import argparse
import datetime
import os
import sys

import config_parser.parser as ConfigParser
import ports_scanner.ports as NetworkScanner
from scan.scan import Scan
from ssh.ssh import SSHConnection
from commands.command_monitor import CommandMonitor
<<<<<<< HEAD
=======
import network_scanner.network_scan as LocalNetworkScanner
import ddos.ddos_attack as DDoSAttack
>>>>>>> e6aaa5a (Push Projet Final)

def print_ascii_art():
    print(r" ________  ________  ________  ________   ________  ___    ___ ")
    print(r"|\   ____\|\   ____\|\   __  \|\   ___  \|\   __  \|\  \  /  /|")
    print(r"\ \  \___|\ \  \___|\ \  \|\  \ \  \\ \  \ \  \|\  \ \  \/  / /")
    print(r" \ \_____  \ \  \    \ \   __  \ \  \\ \  \ \   ____\ \    / / ")
    print(r"  \|____|\  \ \  \____\ \  \ \  \ \  \\ \  \ \  \___|\/  /  /  ")
    print(r"    ____\_\  \ \_______\ \__\ \__\ \__\\ \__\ \__\ __/  / /    ")
    print(r"   |\_________\|_______|\|__|\|__|\|__| \|__|\|__||\___/ /     ")
    print(r"   \|_________|                                   \|___|/      ")
    print(r"                                                                ")
    print(r"                                                                ")

def main():
    print_ascii_art()

    config = ConfigParser.ConfigParser("scanpy.conf")

    # Menu interactif
    print("Sélectionner le type ce que vous souhaitez faire :")
    print("1. Scan de ports")
<<<<<<< HEAD
    print("2. Scan de vulnérabilités (Nessus) :")
    print("3. Tentative de BruteForce via SSH")
    print("4. Surveillance des commandes sur une machine")
=======
    print("2. Scan de vulnérabilités (Nessus)")
    print("3. Tentative de BruteForce via SSH")
    print("4. Surveillance des commandes sur une machine")
    print("5. Scan du réseau local")
    print("6. Lancement d'une attaque DDoS")  # Nouvelle option ajoutée
>>>>>>> e6aaa5a (Push Projet Final)
    choice = input("Entrez le numéro choisi: ")

    if choice == '1':
        ip = input("Entrez l'adresse IP à scanner: ")
<<<<<<< HEAD
        print("[+] Port scan selected.")
=======
        print("[+] Scan de port sélectionné.")
>>>>>>> e6aaa5a (Push Projet Final)
        start_port = config.get("PortScan", "start_port")
        end_port = config.get("PortScan", "end_port")
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.datetime.now().strftime('%H-%M-%S')
        scan_dir = f"results/scans_de_ports/{date_str}/{time_str}"
        if not os.path.exists(scan_dir):
            os.makedirs(scan_dir)
        port_scan = NetworkScanner.PortScanner(
            ip, int(start_port), int(end_port), config.get("PortScan", "scan_args")
        )
        open_ports = port_scan.scan_ports()
        report_path = f"{scan_dir}/{ip}.pdf"
        port_scan.export_scan(report_path)
<<<<<<< HEAD
=======
        print(f"[+] Scan de port exporté ici : {report_path}")
>>>>>>> e6aaa5a (Push Projet Final)
    elif choice == '2':
        ip = input("Entrez l'adresse IP à scanner: ")
        username = input("Entrez l'ID pour le scan de vulnérabilités: ")
        password = input("Entrez le mot de passe pour le scan de vulnérabilités: ")
<<<<<<< HEAD
        print("[+] Vulnerability scan selected.")
=======
        print("[+] Scan de vulnérabilités sélectionné.")
>>>>>>> e6aaa5a (Push Projet Final)
        target_dir = f"results/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        # Create a target file
        with open(f"{target_dir}/targets.txt", "w") as f:
            f.write(ip)
        scan = Scan(
            username=username,
            password=password,
            targets_dir=target_dir,
            date=datetime.datetime.now().strftime("%Y.%m.%d"),
            work_path=config.get("VulnScan", "workpath"),
            configuration_file=config,
        )
        scan.main()
    elif choice == '3':
        ip = input("Entrez l'adresse IP à scanner: ")
<<<<<<< HEAD
        print("[+] SSH brute force selected.")
        ssh = SSHConnection(ip)
        ssh.bruteforce()
=======
        print("[+] Attaque par BruteForce sélectionné.")
        ssh = SSHConnection(ip)
        ssh.bruteforce()
        print(f"[+] Résultat de l'attaque par BruteForce : {ip} (not saved to a specific file)")
>>>>>>> e6aaa5a (Push Projet Final)
    elif choice == '4':
        ip = input("Entrez l'adresse IP de la machine à surveiller: ")
        username = input("Entrez le nom d'utilisateur SSH: ")
        password = input("Entrez le mot de passe SSH: ")
        print("[+] Surveillance des commandes sélectionnée.")
        monitor = CommandMonitor(ip, username, password)
        save_dir = f"results/commands/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(save_dir):
<<<<<<< HEAD
            print(f"[+] Creating directory {save_dir}")
            os.makedirs(save_dir)
        save_path = f"{save_dir}/{datetime.datetime.now().strftime('%H-%M-%S')}_commands.log"
        print(f"[+] Save path set to {save_path}")
        try:
            monitor.connect()
            monitor.monitor_commands("/root/.bash_history", save_path)
=======
            print(f"[+] Création d'un répertoire {save_dir}")
            os.makedirs(save_dir)
        save_path = f"{save_dir}/{datetime.datetime.now().strftime('%H-%M-%S')}_commands.log"
        print(f"[+] Chemin d'enresgitrement défini sur : {save_path}")
        try:
            monitor.connect()
            monitor.monitor_commands("/root/.bash_history", save_path)
            print(f"[+] Rapport de Monitoring de commandes sauvegardé ici : {save_path}")
>>>>>>> e6aaa5a (Push Projet Final)
        except Exception as e:
            print(f"[-] Error: {e}")
        finally:
            monitor.close()
<<<<<<< HEAD
    else:
        print("Invalid choice. Exiting.")
=======
    elif choice == '5':
        network = input("Entrez le réseau (e.g., 192.168.1.0/24): ")
        print("[+] Scan ARP sélectionné.")
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.datetime.now().strftime('%H-%M-%S')
        scan_dir = f"results/network_scan/{date_str}/{time_str}"
        if not os.path.exists(scan_dir):
            os.makedirs(scan_dir)
        network_scan = LocalNetworkScanner.LocalNetworkScanner(network)
        devices = network_scan.scan_network()
        report_path = f"{scan_dir}/network_scan"
        network_scan.generate_report(report_path)
        print(f"[+] Rapport du Scan ARP exporté ici : {report_path}.pdf")
    elif choice == '6':
        target_ip = input("Entrez l'adresse IP cible: ")
        target_port = input("Entrez le port cible: ")
        mode = input("Entrez le mode d'attaque (flood/no-flood): ").strip().lower()
        flood = mode == "flood"
        print("[+] Simuler une attaque DDoS sélectionnée.")
        DDoSAttack.ddos_attack(target_ip, target_port, flood=flood)
    else:
        print("IChoix invalide - Exit.")
>>>>>>> e6aaa5a (Push Projet Final)
        sys.exit(1)

if __name__ == "__main__":
    main()
