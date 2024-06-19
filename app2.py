import customtkinter as ctk
from tkinter import scrolledtext, messagebox
import threading
import datetime
import os
import sys
import webbrowser
from pprint import pformat

import config_parser.parser as ConfigParser
import ports_scanner.ports as NetworkScanner
from scan.scan import Scan
from ssh.ssh import SSHConnection
from commands.command_monitor import CommandMonitor
import network_scanner.network_scan as LocalNetworkScanner
import ddos.ddos_attack as DDoSAttack

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class RedirectOutput:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, message):
        self.widget.insert(ctk.END, message, (self.tag,))
        self.widget.see(ctk.END)

    def flush(self):
        pass

class InputDialog(ctk.CTkToplevel):
    def __init__(self, parent, prompt):
        super().__init__(parent)
        self.title("Input")
        self.geometry("300x150")
        self.prompt = prompt
        self.value = None
        
        self.label = ctk.CTkLabel(self, text=self.prompt)
        self.label.pack(pady=20)
        
        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=10)
        
        self.button = ctk.CTkButton(self, text="OK", command=self.on_ok)
        self.button.pack(pady=10)
        
        self.transient(parent)
        self.grab_set()
        self.entry.focus_set()
        self.wait_window(self)

    def on_ok(self):
        self.value = self.entry.get()
        self.destroy()

class ScanPyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ScanPy")
        self.geometry("1200x700")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create navigation frame
        self.nav_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nswe")
        self.nav_frame.grid_rowconfigure(0, minsize=10)  # Empty row with minsize as spacing
        self.nav_frame.grid_rowconfigure(8, weight=1)  # Empty row as spacing

        # Add navigation buttons
        self.create_nav_button("Scan de ports", self.port_scan, 1)
        self.create_nav_button("Scan de vulnérabilités", self.vuln_scan, 2)
        self.create_nav_button("Scan du réseau local", self.network_scan, 3)
        self.create_nav_button("BruteForce SSH", self.ssh_bruteforce, 4)
        self.create_nav_button("Surveillance des commandes", self.command_monitor, 5)
        self.create_nav_button("Attaque DDoS", self.ddos_attack, 6)
        self.create_nav_button("ARRET", self.stop_tasks, 7)
        self.create_nav_button("Réinitialiser", self.reset_output, 8)

        # Create output frame
        self.output_frame = ctk.CTkFrame(self, corner_radius=0)
        self.output_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        # Create scrolled text for output display
        self.output_text = scrolledtext.ScrolledText(self.output_frame, wrap="word", font=("Consolas", 12), bg="white", fg="black")
        self.output_text.grid(row=0, column=0, sticky="nswe")

        # Redirect stdout and stderr
        sys.stdout = RedirectOutput(self.output_text, "stdout")
        sys.stderr = RedirectOutput(self.output_text, "stderr")

        self.current_thread = None

    def create_nav_button(self, text, command, row):
        button = ctk.CTkButton(self.nav_frame, text=text, command=command, width=200, height=40)
        button.grid(row=row, column=0, pady=10, padx=20)

    def port_scan(self):
        self.run_in_thread(self.run_port_scan)

    def vuln_scan(self):
        self.run_in_thread(self.run_vuln_scan)

    def ssh_bruteforce(self):
        self.run_in_thread(self.run_ssh_bruteforce)

    def command_monitor(self):
        self.run_in_thread(self.run_command_monitor)

    def network_scan(self):
        self.run_in_thread(self.run_network_scan)

    def ddos_attack(self):
        self.run_in_thread(self.run_ddos_attack)

    def reset_output(self):
        self.output_text.delete(1.0, ctk.END)

    def stop_tasks(self):
        if self.current_thread:
            self.current_thread.do_run = False
            self.current_thread = None
        self.log_output("[+] All tasks have been stopped.")

    def run_in_thread(self, func):
        self.current_thread = threading.Thread(target=func)
        self.current_thread.start()

    def run_port_scan(self):
        ip = self.get_input("Entrez l'adresse IP à scanner:")
        self.log_output(f"[+] Scan de ports sélectionné pour : {ip}")
        config = ConfigParser.ConfigParser("scanpy.conf")
        start_port = config.get("PortScan", "start_port")
        end_port = config.get("PortScan", "end_port")
        port_scan = NetworkScanner.PortScanner(ip, int(start_port), int(end_port), config.get("PortScan", "scan_args"))
        open_ports = port_scan.scan_ports()
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.datetime.now().strftime('%H-%M-%S')
        scan_dir = f"results/scans_de_ports/{date_str}/{time_str}"
        if not os.path.exists(scan_dir):
            os.makedirs(scan_dir)
        report_path = f"{scan_dir}/{ip}"
        port_scan.export_scan(report_path)
        self.log_output(f"Ports ouvert:\n{pformat(open_ports)}")
        self.log_output(f"Résultats du scan de ports exporté ici ", report_path + ".pdf", True)

    def run_vuln_scan(self):
        ip = self.get_input("Entrez l'adresse IP à scanner:")
        username = self.get_input("Entrez l'ID pour le scan de vulnérabilités:")
        password = self.get_input("Entrez le mot de passe pour le scan de vulnérabilités:")
        self.log_output(f"[+] Scan de Vulnérabilités sélectionné pour l'IP suivante : {ip}")
        config = ConfigParser.ConfigParser("scanpy.conf")
        target_dir = f"results/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        with open(f"{target_dir}/targets.txt", "w") as f:
            f.write(ip)
        scan = Scan(username=username, password=password, targets_dir=target_dir,
                    date=datetime.datetime.now().strftime("%Y.%m.%d"),
                    work_path=config.get("VulnScan", "workpath"), configuration_file=config)
        
        # Redirect the log to the GUI
        def new_log_function(message):
            self.log_output(message)
        
        scan.log = new_log_function
        scan.main()
        self.log_output(f"Scan de Vulnérabilité complété pour l'IP : {ip}")

    def run_ssh_bruteforce(self):
        ip = self.get_input("Entrez l'adresse IP à scanner:")
        self.log_output(f"[+] BruteForce SSH sélectionné pour l'IP : {ip}")
        ssh = SSHConnection(ip)
        ssh.bruteforce()
        self.log_output(f"BruteForce SSH complété pour l'IP : {ip}")

    def run_command_monitor(self):
        ip = self.get_input("Entrez l'adresse IP de la machine à surveiller:")
        username = self.get_input("Entrez le nom d'utilisateur SSH:")
        password = self.get_input("Entrez le mot de passe SSH:")
        self.log_output(f"[+] Monitoring de commandes sélectionné pour l'IP: {ip}")
        monitor = CommandMonitor(ip, username, password)
        save_dir = f"results/commands/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = f"{save_dir}/{datetime.datetime.now().strftime('%H-%M-%S')}_commands.log"
        try:
            monitor.connect()
            monitor.monitor_commands("/root/.bash_history", save_path)
            self.log_output(f"Monitoring de commandes complété pour l'IP: {ip}")
            self.log_output(f"Rapport sauvegardé ici ", save_path, True)
        except Exception as e:
            self.log_output(f"[-] Error: {e}")
        finally:
            monitor.close()

    def run_network_scan(self):
        network = self.get_input("Entrez le réseau (e.g., 192.168.1.0/24):")
        self.log_output(f"[+] Scan ARP sélectionné pour le réseau : {network}")
        network_scan = LocalNetworkScanner.LocalNetworkScanner(network)
        devices = network_scan.scan_network()
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.datetime.now().strftime('%H-%M-%S')
        scan_dir = f"results/network_scan/{date_str}/{time_str}"
        if not os.path.exists(scan_dir):
            os.makedirs(scan_dir)
        report_path = f"{scan_dir}/network_scan"
        network_scan.generate_report(report_path)
        self.log_output(f"Appareil trouvé :\n{pformat(devices)}")
        self.log_output(f"Rapport exporté ici ", report_path + ".pdf", True)

    def run_ddos_attack(self):
        target_ip = self.get_input("Entrez l'adresse IP cible:")
        target_port = self.get_input("Entrez le port cible:")
        packet_count = self.get_input("Entrez le nombre de paquets:")
        self.log_output(f"[+] Attaque DDoS sur l'adresse suivante : {target_ip}")
        DDoSAttack.ddos_attack(target_ip, target_port, packet_count)
        self.log_output(f"Attaque DDoS Complété sur l'adresse : {target_ip}")

    def log_output(self, message, path=None, clickable=False):
        if clickable:
            self.output_text.insert(ctk.END, message)
            self.output_text.insert(ctk.END, path + "\n", ('link',))
            self.output_text.tag_config('link', foreground="blue", underline=True)
            self.output_text.tag_bind('link', '<Enter>', lambda e: self.output_text.config(cursor="hand2"))
            self.output_text.tag_bind('link', '<Leave>', lambda e: self.output_text.config(cursor=""))
            self.output_text.tag_bind('link', '<Button-1>', lambda e, path=path: self.open_path(path))
        else:
            self.output_text.insert(ctk.END, message + "\n")
        self.output_text.see(ctk.END)

    def get_input(self, prompt):
        dialog = InputDialog(self, prompt)
        return dialog.value

    def open_path(self, path):
        if path.endswith(".pdf"):
            os.system(f"xdg-open {path}")
        else:
            folder = os.path.dirname(path)
            webbrowser.open(f"file://{os.path.realpath(folder)}")

if __name__ == "__main__":
    app = ScanPyApp()
    app.mainloop()
