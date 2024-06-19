import customtkinter as ctk
import sys
import os
from threading import Thread

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ports_scanner.ports import PortScanner
from nessus_api.nessus_api import NessusAPI
from commands.command_monitor import CommandMonitor
from ssh.ssh import SSHConnection

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Toolbox Application")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        self.button_frame = ctk.CTkFrame(self, width=200)
        self.button_frame.pack(side="left", fill="y")

        # Buttons
        self.port_scan_button = ctk.CTkButton(self.button_frame, text="Scan de ports", command=self.run_port_scan)
        self.port_scan_button.pack(pady=12, padx=10, fill="x")

        self.vuln_scan_button = ctk.CTkButton(self.button_frame, text="Scan de vulnérabilités (Nessus)", command=self.run_vuln_scan)
        self.vuln_scan_button.pack(pady=12, padx=10, fill="x")

        self.bruteforce_button = ctk.CTkButton(self.button_frame, text="Tentative de BruteForce via SSH", command=self.run_bruteforce)
        self.bruteforce_button.pack(pady=12, padx=10, fill="x")

        self.command_monitor_button = ctk.CTkButton(self.button_frame, text="Surveillance des commandes sur une machine de test", command=self.run_command_monitor)
        self.command_monitor_button.pack(pady=12, padx=10, fill="x")

        # Frame for logs
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Text box for logs
        self.log_text = ctk.CTkTextbox(self.log_frame)
        self.log_text.pack(fill="both", expand=True)

    def log_message(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def run_port_scan(self):
        def task():
            target = "192.168.2.136"
            start_port = 20
            end_port = 80
            scan_arguments = "-sV"
            port_scanner = PortScanner(target, start_port, end_port, scan_arguments)
            port_scanner.scan_ports()
            self.log_message("Scan de ports terminé.")
            port_scanner.export_scan("/home/toolbox/ScanPy4/results/port_scan_results.pdf")
            self.log_message("Résultats du scan de ports exportés.")

        Thread(target=task).start()

    def run_vuln_scan(self):
        def task():
            nessus_api = NessusAPI()
            self.log_message("Scan de vulnérabilités commencé.")
            # Utiliser les méthodes de NessusAPI pour exécuter un scan de vulnérabilité
            self.log_message("Scan de vulnérabilités terminé.")

        Thread(target=task).start()

    def run_bruteforce(self):
        def task():
            ssh_connection = SSHConnection(ip_address="192.168.2.136")
            ssh_connection.bruteforce()
            self.log_message("BruteForce SSH terminé.")

        Thread(target=task).start()

    def run_command_monitor(self):
        def task():
            command_monitor = CommandMonitor()
            command_monitor.monitor_commands("/home/toolbox/ScanPy4/results/command_monitor_report")
            self.log_message("Surveillance des commandes terminée.")

        Thread(target=task).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
