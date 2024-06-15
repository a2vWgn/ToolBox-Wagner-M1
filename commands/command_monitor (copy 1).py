import paramiko
import time

class CommandMonitor:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh_client = None
        self.sftp_client = None

    def connect(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.hostname, username=self.username, password=self.password)
            self.sftp_client = self.ssh_client.open_sftp()
            print("[+] Connected to SSH.")
        except Exception as e:
            print(f"[-] Error connecting to SSH: {e}")
            raise

    def monitor_commands(self, remote_file_path, save_path):
        try:
            print("[+] Monitoring started.")
            previous_size = 0
            while True:
                current_size = self.sftp_client.stat(remote_file_path).st_size
                if current_size > previous_size:
                    with self.sftp_client.open(remote_file_path, 'r') as remote_file:
                        remote_file.seek(previous_size)
                        new_data = remote_file.read().decode('utf-8')
                        previous_size = current_size
                        with open(save_path, 'a') as local_file:
                            local_file.write(new_data)
                time.sleep(1)
        except KeyboardInterrupt:
            print("[+] Monitoring stopped.")
        except Exception as e:
            print(f"[-] Error processing line: {e}")
        finally:
            self.sftp_client.close()
            self.ssh_client.close()
            print("[+] SSH connection closed.")

    def close(self):
        if self.sftp_client:
            self.sftp_client.close()
        if self.ssh_client:
            self.ssh_client.close()
