import argparse
import datetime
import os
import sys

import config_parser.parser as ConfigParser
import ports_scanner.ports as NetworkScanner
from scan.scan import Scan
from ssh.ssh import SSHConnection
from commands.command_monitor import CommandMonitor

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
    print("2. Scan de vulnérabilités (Nessus) :")
    print("3. Tentative de BruteForce via SSH")
    print("4. Surveillance des commandes sur une machine")
    choice = input("Entrez le numéro choisi: ")

    if choice == '1':
        ip = input("Entrez l'adresse IP à scanner: ")
        print("[+] Port scan selected.")
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
    elif choice == '2':
        ip = input("Entrez l'adresse IP à scanner: ")
        username = input("Entrez l'ID pour le scan de vulnérabilités: ")
        password = input("Entrez le mot de passe pour le scan de vulnérabilités: ")
        print("[+] Vulnerability scan selected.")
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
        print("[+] SSH brute force selected.")
        ssh = SSHConnection(ip)
        ssh.bruteforce()
    elif choice == '4':
        ip = input("Entrez l'adresse IP de la machine à surveiller: ")
        username = input("Entrez le nom d'utilisateur SSH: ")
        password = input("Entrez le mot de passe SSH: ")
        print("[+] Surveillance des commandes sélectionnée.")
        monitor = CommandMonitor(ip, username, password)
        save_dir = f"results/commands/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(save_dir):
            print(f"[+] Creating directory {save_dir}")
            os.makedirs(save_dir)
        save_path = f"{save_dir}/{datetime.datetime.now().strftime('%H-%M-%S')}_commands.log"
        print(f"[+] Save path set to {save_path}")
        try:
            monitor.connect()
            monitor.monitor_commands("/root/.bash_history", save_path)
        except Exception as e:
            print(f"[-] Error: {e}")
        finally:
            monitor.close()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
