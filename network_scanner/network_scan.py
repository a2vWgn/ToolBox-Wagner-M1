import os
import subprocess
from jinja2 import Environment, FileSystemLoader
import pdfkit

class LocalNetworkScanner:
    def __init__(self, network):
        self.network = network
        self.devices = []

    def scan_network(self):
        command = f"sudo arp-scan -l"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        lines = result.stdout.splitlines()
        
        for line in lines:
            if 'VMware' in line:  # Vous devrez peut-être ajuster cela pour correspondre au format de sortie réel
                parts = line.split()
                ip = parts[0]
                mac = parts[1]
                vendor = ' '.join(parts[2:])
                self.devices.append({'ip': ip, 'mac': mac, 'vendor': vendor})
                
        return self.devices

    def generate_report(self, output_path):
        env = Environment(loader=FileSystemLoader('template'))
        template = env.get_template('scan_local_arp.html')
        html_out = template.render(network=self.network, devices=self.devices)

        with open(output_path + '.html', 'w') as f:
            f.write(html_out)

        pdfkit.from_file(output_path + '.html', output_path + '.pdf')

        os.remove(output_path + '.html')
